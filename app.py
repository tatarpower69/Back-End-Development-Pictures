from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
pictures = {1: {'id': 1, 'title': 'Band rehearsal', 'url': 'https://picsum.photos/id/250/800/500'}, 2: {'id': 2, 'title': 'Live concert', 'url': 'https://picsum.photos/id/453/800/500'}}
@app.get('/health')
def health(): return jsonify(status='OK')
@app.get('/count')
def count(): return jsonify(count=len(pictures))
@app.get('/pictures')
def all_pictures(): return jsonify(list(pictures.values()))
@app.get('/pictures/<int:picture_id>')
def get_picture(picture_id):
    return (jsonify(pictures[picture_id]), 200) if picture_id in pictures else (jsonify(error='Not found'), 404)
@app.post('/pictures')
def create_picture():
    data=request.get_json(silent=True) or {}
    if not data.get('title') or not data.get('url'): return jsonify(error='title and url required'),400
    key=max(pictures,default=0)+1; pictures[key]={'id':key,'title':data['title'],'url':data['url']}
    return jsonify(pictures[key]),201
@app.put('/pictures/<int:picture_id>')
def update_picture(picture_id):
    if picture_id not in pictures: return jsonify(error='Not found'),404
    pictures[picture_id].update({k:v for k,v in (request.get_json(silent=True) or {}).items() if k in ('title','url')})
    return jsonify(pictures[picture_id])
@app.delete('/pictures/<int:picture_id>')
def delete_picture(picture_id):
    if picture_id not in pictures: return jsonify(error='Not found'),404
    del pictures[picture_id];return jsonify(message='Deleted')
if __name__=='__main__': app.run(host='0.0.0.0',port=5001)
