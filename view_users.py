from app import create_app
from models import User

app = create_app()

with app.app_context():

    users = User.query.all()

    print("\nUSERS")
    print("=" * 30)

    for user in users:
        print(
            user.id,
            user.username,
            user.password_hash
        )
        