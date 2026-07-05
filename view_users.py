from app import create_app
from models import User

app = create_app()

with app.app_context():

    users = User.query.all()

    print("\nUSERS")
    print("=" * 50)

    for user in users:
        print(
            f"ID: {user.id} | "
            f"Username: {user.username} | "
            f"Admin: {user.is_admin}"
        )
        