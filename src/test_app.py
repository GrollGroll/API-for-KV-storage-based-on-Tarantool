from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# Тест для эндпоинта /login
def test_login_success():
    response = client.post('/api/login', data={"username": "admin", "password": "presale"})
    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_login_wrong_password():
    response = client.post('/api/login', data={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Wrong password"}


def test_login_user_not_found():
    response = client.post('/api/login', data={"username": "unknown", "password": "password"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username not found"}


# Тест для эндпоинта /write
def test_write_data():
    login_response = client.post('/api/login', data={"username": "admin", "password": "presale"})
    token = login_response.json()['access_token']

    response = client.post(
        '/api/write',
        json={"data": {"key1": "value1", "key2": "value2"}},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


# Тест для эндпоинта /read
def test_read_data():
    login_response = client.post('/api/login', data={"username": "admin", "password": "presale"})
    token = login_response.json()['access_token']

    response = client.post(
        '/api/read',
        json={"keys": ["key1", "key2"]},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "key1": "value1",
            "key2": "value2"
        }
    }


def test_read_nonexistent_key():
    login_response = client.post('/api/login', data={"username": "admin", "password": "presale"})
    token = login_response.json()['access_token']

    response = client.post(
        '/api/read',
        json={"keys": ["nonexistent_key"]},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "nonexistent_key": None
        }
    }
