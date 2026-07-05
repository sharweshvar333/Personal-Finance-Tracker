from flask import Flask, render_template

from app.extensions import db, csrf, login_manager, limiter
from app.blueprints.budget import budget_bp
from app.blueprints.transactions import transactions_bp
from app.blueprints.api import api_bp
from app.blueprints.auth import auth_bp
from app.blueprints.savings import savings_bp
from app.blueprints.admin import admin_bp

from app.scheduler import start_scheduler

from app.services.exchange_service import get_usd_rate

import time


def create_app():

    app = Flask(__name__)
    app.config["START_TIME"] = time.time()

    app.config.from_object(
        "config.DevelopmentConfig"
    )

    db.init_app(app)
    csrf.init_app(app)

    from models import User, Transaction

    login_manager.init_app(app)

    limiter.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        import models
        db.create_all()

    # -----------------------
    # Start APScheduler
    # -----------------------
    start_scheduler(app)

    app.register_blueprint(budget_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(savings_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():

        transactions = Transaction.query.all()

        total_income = sum(
            t.amount
            for t in transactions
            if t.transaction_type.lower() == "income"
        )

        total_expense = sum(
            t.amount
            for t in transactions
            if t.transaction_type.lower() == "expense"
        )

        balance = total_income - total_expense

        usd_rate = get_usd_rate()

        total_expense_usd = total_expense * usd_rate

        return render_template(
            "index.html",
            total_income=total_income,
            total_expense=total_expense,
            balance=balance,
            usd_rate=usd_rate,
            total_expense_usd=total_expense_usd
        )

    @app.errorhandler(404)
    def not_found(error):
        return {
            "error": "Resource not found"
        }, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {
            "error": "Internal server error"
        }, 500

    return app
