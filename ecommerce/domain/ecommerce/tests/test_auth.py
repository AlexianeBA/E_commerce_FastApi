from fastapi import FastAPI


from fastapi.testclient import TestClient


from infrastructure.api.dto.dto_auth import Login

app = FastAPI()
client = TestClient(app)


def test_login():
    login_data = Login(username="test_user", password="test_password")
    response = client.post("/login", json=login_data.dict())
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}


def test_forgot_password():
    email = "test@example.com"
    response = client.post("/forgot_password", json={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset email sent"}


def test_reset_password():
    user_id = 123
    new_password = "new_password"
    response = client.post(
        "/reset_password", json={"user_id": user_id, "new_password": new_password}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset successful"}
