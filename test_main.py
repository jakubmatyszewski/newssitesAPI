from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_is_up():
    response = client.get('/')
    assert response.status_code == 200
    assert '<h1>News Sites API</h1>' in response.text


def test_get_news_headline():
    with TestClient(app) as client:
        response = client.get('/news?page=tvn24')
        assert response.status_code == 200
        assert len(response.json()) == 1


def test_get_news_headlines_closest_to_date():
    with TestClient(app) as client:
        response = client.get('/news?site=tvn24&date=2021-01-01&limit=10')
        assert response.status_code == 200
        assert len(response.json()) == 10

        response = client.get('/news?site=tvn24&date=2021-01-01T12:30:00\
&limit=10')
        assert response.status_code == 200
        assert len(response.json()) == 10


def test_form_post():
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    test_request_payload = {"date": "2021-01-01T12:00", "site": "tvn24"}
    response = client.post('/', data=test_request_payload, headers=headers)
    assert response.status_code == 200
