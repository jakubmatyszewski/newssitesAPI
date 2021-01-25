from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_hello_world():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_news_headline():
    with TestClient(app) as client:
        response = client.get('/news?page=tvn24')
        assert response.status_code == 200
        assert len(response.json()) == 1


def test_get_news_headlines_closest_to_date():
    with TestClient(app) as client:
        response = client.get('/news?site=tvn24&date=2021-01-23&limit=10')
        assert response.status_code == 200
        assert len(response.json()) == 10

        response = client.get('/news?site=tvn24&date=2021-01-23T12:30:00\
&limit=10')
        assert response.status_code == 200
        assert len(response.json()) == 10
