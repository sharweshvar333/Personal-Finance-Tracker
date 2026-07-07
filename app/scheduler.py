from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from datetime import date, timedelta

from app.extensions import db
from models import Transaction


def budget_summary():
    """
    Calculates daily budget summary from DB.
    """

    try:
        transactions = Transaction.query.all()

        income = sum(
            t.amount
            for t in transactions
            if t.transaction_type
            and t.transaction_type.lower() == "income"
        )

        expense = sum(
            t.amount
            for t in transactions
            if t.transaction_type
            and t.transaction_type.lower() == "expense"
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
    Simulated monthly email alert.
    """

    try:
        current_app.logger.info("===== Monthly Budget Alert =====")
        current_app.logger.info("To: sharwesh@example.com")
        current_app.logger.info("Subject: Monthly Budget Alert")
        current_app.logger.info("Please review your monthly expenses.")

    except Exception as e:
        current_app.logger.error(f"Error in monthly_budget_alert: {e}")


def process_recurring_transactions():
    """
    Automatically generates recurring transactions.
    """

    try:

        today = date.today()

        recurring_transactions = Transaction.query.filter_by(
            is_recurring=True
        ).all()

        for transaction in recurring_transactions:

            if transaction.last_processed is None:
                last = transaction.start_date
            else:
                last = transaction.last_processed

            if last is None:
                continue

            if transaction.recurrence == "daily":
                next_due = last + timedelta(days=1)

            elif transaction.recurrence == "weekly":
                next_due = last + timedelta(weeks=1)

            elif transaction.recurrence == "monthly":
                next_due = last + timedelta(days=30)

            else:
                continue

            if next_due <= today:

                new_transaction = Transaction(
                    amount=transaction.amount,
                    category=transaction.category,
                    transaction_type=transaction.transaction_type,
                    date=today,
                    is_recurring=False
                )

                db.session.add(new_transaction)

                transaction.last_processed = today

        db.session.commit()

        current_app.logger.info(
            "Recurring transaction check completed."
        )

    except Exception as e:
        current_app.logger.error(
            f"Error processing recurring transactions: {e}"
        )


def start_scheduler(app):

    scheduler = BackgroundScheduler()

    def scheduled_job():
        with app.app_context():
            budget_summary()

    def monthly_job():
        with app.app_context():
            monthly_budget_alert()

    def recurring_job():
        with app.app_context():
            process_recurring_transactions()

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

    scheduler.add_job(
        recurring_job,
        trigger="interval",
        seconds=15,
        id="recurring_transactions"
    )

    scheduler.start()

    return scheduler
