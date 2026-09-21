import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def unique_user():
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"

    return {
        "username": username,
        "full_name": "CyberShield TestUser",
        "email": email,
        "password": "Test@12345",
    }

def test_register_user():
    payload = unique_user()

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code in {200, 201}

    data = response.json()

    assert isinstance(data, dict)

def test_login_registered_user():
    payload = unique_user()

    register_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert register_response.status_code in {200, 201}

    login_response = client.post(
        "/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert isinstance(data, dict)

def test_register_duplicate_email():
    payload = unique_user()

    first_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert first_response.status_code in {200, 201}

    second_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert second_response.status_code in {
        400,
        409,
        422,
    }

def test_login_invalid_password():
    payload = unique_user()

    register_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert register_response.status_code in {200, 201}

    response = client.post(
        "/auth/login",
        json={
            "email": payload["email"],
            "password": "WrongPassword@999",
        },
    )

    assert response.status_code in {
        400,
        401,
        403,
    }

def test_login_unknown_user():
    response = client.post(
        "/auth/login",
        json={
            "email": f"unknown_{uuid.uuid4().hex[:8]}@example.com",
            "password": "Test@12345",
        },
    )

    assert response.status_code in {
        400,
        401,
        403,
    }
