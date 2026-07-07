from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_babel import Babel


# Database
db = SQLAlchemy()


# CSRF Protection
csrf = CSRFProtect()


# Login Manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"


# Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[]
)


# Flask-Babel
babel = Babel()