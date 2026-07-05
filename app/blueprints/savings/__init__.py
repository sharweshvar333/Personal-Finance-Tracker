from flask import Blueprint

savings_bp = Blueprint(
    "savings",
    __name__
)

from . import routes
