from apscheduler.schedulers.background import BackgroundScheduler
from models import Transaction


def budget_summary():

    transactions = Transaction.query.all()

    income = sum(
        t.amount
        for t in transactions
        if t.transaction_type.lower() == "income"
    )

    expense = sum(
        t.amount
        for t in transactions
        if t.transaction_type.lower() == "expense"
    )

    balance = income - expense

    print("\n==============================")
    print("💰 Daily Budget Summary")
    print("==============================")
    print(f"Income  : ₹{income:.2f}")
    print(f"Expense : ₹{expense:.2f}")
    print(f"Balance : ₹{balance:.2f}")
    print("==============================\n")

def monthly_budget_alert():

    print("\n===================================")
    print("📧 Monthly Budget Alert")
    print("===================================")
    print("To      : sharwesh@example.com")
    print("Subject : Monthly Budget Alert")
    print()
    print("Hello,")
    print("This is your monthly budget reminder.")
    print("Please review your expenses.")
    print()
    print("Regards,")
    print("Finance Tracker")
    print("===================================\n")

def start_scheduler(app):

    scheduler = BackgroundScheduler()

    def scheduled_job():
        with app.app_context():
            budget_summary()

    scheduler.add_job(
        scheduled_job,
        trigger="interval",
        seconds=30
    )

    def monthly_job():
        with app.app_context():
            monthly_budget_alert()

    scheduler.add_job(
        monthly_job,
        trigger="interval",
        seconds=60
    )    

    scheduler.start()

    return scheduler