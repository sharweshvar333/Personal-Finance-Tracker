from flask import Flask, render_template, Response, g, request
import time
import logging
from logging.handlers import RotatingFileHandler
import os

from app.extensions import db, csrf, login_manager, limiter, babel
from app.blueprints.budget import budget_bp
from app.blueprints.transactions import transactions_bp
from app.blueprints.api import api_bp
from app.blueprints.auth import auth_bp
from app.blueprints.savings import savings_bp
from app.blueprints.admin import admin_bp

from app.scheduler import start_scheduler
from app.services.exchange_service import get_usd_rate

from flasgger import Swagger

from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST
)

from app.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY
)


def create_app():

    app = Flask(__name__)

    app.config["START_TIME"] = time.time()

    app.config.from_object(
        "config.DevelopmentConfig"
    )

    # ----------------------------
    # Logging Configuration
    # ----------------------------
    if not os.path.exists("logs"):
        os.mkdir("logs")
        
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10240,
        backupCount=5
    )

    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s"
        )
    )

    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    app.logger.info("Finance Tracker Started")

    db.init_app(app)
    csrf.init_app(app)

    from models import User, Transaction

    login_manager.init_app(app)
    limiter.init_app(app)
    babel.init_app(app)

    Swagger(app)

    app.config["BABEL_DEFAULT_LOCALE"] = "en"
    app.config["BABEL_DEFAULT_TIMEZONE"] = "Asia/Kolkata"

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

    # -----------------------
    # Register Blueprints
    # -----------------------
    app.register_blueprint(budget_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(savings_bp)
    app.register_blueprint(admin_bp)

    # =====================================================
    # PROMETHEUS METRICS
    # =====================================================

    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request
    def after_request(response):

        if hasattr(g, "start_time"):

            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.path
            ).inc()

            REQUEST_LATENCY.observe(
                time.time() - g.start_time
            )

        return response

    @app.route("/metrics")
    def metrics():

        return Response(
            generate_latest(),
            mimetype=CONTENT_TYPE_LATEST
        )

    # =====================================================
    # HOME
    # =====================================================

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

    # =====================================================
    # ERROR HANDLERS
    # =====================================================

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
    