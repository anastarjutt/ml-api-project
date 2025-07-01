from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

api_key = 'secretkey'

def check_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'Status':'OK'}

def test_v1_predict():
    files = {'file':('test.jpg',b'fakeimagedata','image/jpeg')}
    headers = {'X-API-KEY':api_key}
    response = client.post('/V1/predict',files=files,headers=headers)
    assert response.status_code in (200,422)

def test_v2_predict():
    files = {'file':('test.jpeg',b'fakeimagedata','image/jpeg')}
    headers = {'X-API-KEY':api_key}
    response = client.post('/V2/predict',files=files,headers=headers)
    assert response.status_code == (200,422)

def test_missing_key():
    files = {'file':('test.jpg',b'fakeimagedata','image/jpeg')}
    response = client.post('/V1/predict',files=files)
    assert response.status_code == 401
