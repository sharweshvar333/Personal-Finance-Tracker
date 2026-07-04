from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from models import Transaction


def budget_summary():
    """
    Calculates daily budget summary from DB
    """

    try:
        transactions = Transaction.query.all()

        income = sum(
            t.amount for t in transactions
            if t.transaction_type and t.transaction_type.lower() == "income"
        )

        expense = sum(
            t.amount for t in transactions
            if t.transaction_type and t.transaction_type.lower() == "expense"
        )

        balance = income - expense

        current_app.logger.info("===== Daily Budget Summary =====")
        current_app.logger.info(f"Income  : ₹{income:.2f}")
        current_app.logger.info(f"Expense : ₹{expense:.2f}")
        current_app.logger.info(f"Balance : ₹{balance:.2f}")

    except Exception as e:
        current_app.logger.error(f"Error in budget_summary: {e}")


def monthly_budget_alert():
    """
    Simulated monthly email alert (demo version)
    """

    try:
        current_app.logger.info("===== Monthly Budget Alert =====")
        current_app.logger.info("To: sharwesh@example.com")
        current_app.logger.info("Subject: Monthly Budget Alert")
        current_app.logger.info("Please review your monthly expenses.")

    except Exception as e:
        current_app.logger.error(f"Error in monthly_budget_alert: {e}")


def start_scheduler(app):
    scheduler = BackgroundScheduler()

    def scheduled_job():
        with app.app_context():
            budget_summary()

    def monthly_job():
        with app.app_context():
            monthly_budget_alert()

    scheduler.add_job(
        scheduled_job,
        trigger="interval",
        seconds=30,
        id="daily_summary"
    )

    scheduler.add_job(
        monthly_job,
        trigger="interval",
        seconds=60,
        id="monthly_alert"
    )

    scheduler.start()

    return scheduler