from app import create_app
from models import User
from werkzeug.security import check_password_hash

app = create_app()

with app.app_context():

    user = User.query.filter_by(
        username="admin"
    ).first()

    print(
        check_password_hash(
            user.password_hash,
            "admin123"
        )
    )
