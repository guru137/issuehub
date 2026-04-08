from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


#  1. Health check / root test
def test_app_running():
    response = client.get("/")
    assert response.status_code in [200, 404]


#  2. Signup test
def test_signup():
    response = client.post(
        "/signup",
        json={
            "name": "testuser",
            "email": "testuser@gmail.com",
            "password": "test123"
        }
    )
    assert response.status_code in [200, 400]


#  3. Login test
def test_login():
    response = client.post(
        "/login",
        json={
            "email": "testuser@gmail.com",
            "password": "test123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


#  4. Create Project (protected API)
def test_create_project():
    # login first
    login = client.post(
        "/login",
        json={
            "email": "testuser@gmail.com",
            "password": "test123"
        }
    )

    token = login.json()["access_token"]

    response = client.post(
        "/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Project",
            "description": "Demo project"
        }
    )

    assert response.status_code in [200, 400]