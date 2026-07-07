from app import create_app
from models import User
from app.extensions import db

app = create_app()

with app.app_context():

    print("DATABASE URI:")
    print(db.engine.url)

    users = User.query.all()

    print("\nUSERS")
    print("=" * 50)

    for user in users:
        print(
            f"ID: {user.id} | "
            f"Username: {user.username} | "
            f"Admin: {user.is_admin}"
        )
        