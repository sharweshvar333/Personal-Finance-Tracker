from app.extensions import db

def test_register_page_loads(client):
    response = client.get("/auth/register")

    assert response.status_code == 200


def test_login_page_loads(client):
    response = client.get("/auth/login")

    assert response.status_code == 200

from models import User


def test_user_registration(client, app):
    response = client.post(
        "/auth/register",
        data={
            "username": "pytest_user",
            "password": "password123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(username="pytest_user").first()

        assert user is not None    

from werkzeug.security import generate_password_hash


def test_user_login(client, app):

    with app.app_context():

        user = User(
            username="login_user",
            password_hash=generate_password_hash("password123")
        )

        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "login_user",
            "password": "password123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Welcome back!" in response.data

def test_invalid_login(client):

    response = client.post(
        "/auth/login",
        data={
            "username": "wronguser",
            "password": "wrongpassword"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Invalid username or password." in response.data

def test_logout(client, app):

    with app.app_context():

        user = User(
            username="logout_user",
            password_hash=generate_password_hash("password123")
        )

        db.session.add(user)
        db.session.commit()

    client.post(
        "/auth/login",
        data={
            "username": "logout_user",
            "password": "password123"
        },
        follow_redirects=True
    )

    response = client.get(
        "/auth/logout",
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Logged out successfully." in response.data
    
