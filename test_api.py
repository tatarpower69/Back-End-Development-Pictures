import pytest
from app import app, pictures
@pytest.fixture
def client():
    app.config['TESTING']=True
    with app.test_client() as c: yield c
def test_health(client): assert client.get('/health').json['status']=='OK'
def test_count(client): assert isinstance(client.get('/count').json['count'],int)
def test_get_pictures(client): assert client.get('/pictures').status_code==200
def test_get_picture(client): assert client.get('/pictures/1').json['id']==1
def test_get_picture_missing(client): assert client.get('/pictures/9999').status_code==404
def test_get_pictures_is_list(client): assert isinstance(client.get('/pictures').json,list)
def test_get_pictures_content(client): assert 'title' in client.get('/pictures/1').json
def test_post_picture(client): assert client.post('/pictures',json={'title':'Test','url':'https://example.com/a.jpg'}).status_code==201
def test_post_invalid(client): assert client.post('/pictures',json={}).status_code==400
def test_update_picture(client): assert client.put('/pictures/1',json={'title':'Updated'}).json['title']=='Updated'
def test_delete_picture(client):
    response=client.post('/pictures',json={'title':'Delete me','url':'https://example.com/x.jpg'})
    assert client.delete('/pictures/'+str(response.json['id'])).status_code==200
