from werkzeug.security import generate_password_hash

from models import User, Transaction
from app.extensions import db


def login(client):
    return client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "password123"
        },
        follow_redirects=True
    )


def create_user(app):
    with app.app_context():

        user = User.query.filter_by(username="testuser").first()

        if not user:
            user = User(
                username="testuser",
                password_hash=generate_password_hash("password123")
            )

            db.session.add(user)
            db.session.commit()


def test_add_transaction(client, app):

    create_user(app)

    login(client)

    response = client.post(
        "/transactions",
        data={
            "amount": 1000,
            "category": "Food",
            "transaction_type": "expense",
            "date": "2026-07-05"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Transaction added successfully!" in response.data

def test_view_transactions(client, app):

    create_user(app)

    login(client)

    response = client.get(
        "/transactions",
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Transactions" in response.data

def test_dashboard_page(client, app):

    create_user(app)

    login(client)

    response = client.get(
        "/dashboard",
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Dashboard" in response.data
    