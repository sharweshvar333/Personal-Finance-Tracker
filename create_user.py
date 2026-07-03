from app import create_app
from app.extensions import db
from models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    existing_user = User.query.filter_by(
        username="admin"
    ).first()

    if existing_user:
        print("Admin already exists.")

    else:
        admin = User(
            username="admin",
            password_hash=generate_password_hash(
                "admin123"
            )
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully.")
        