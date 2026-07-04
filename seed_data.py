from app import create_app
from app.extensions import db
from models import Budget, Transaction
from datetime import date

# Create Flask app context
app = create_app()

with app.app_context():

    # -----------------------
    # Demo Budgets
    # -----------------------
    budgets = [
        Budget(category="Food", month="2026-06", limit_amount=20000),
        Budget(category="Travel", month="2026-06", limit_amount=30000),
        Budget(category="Shopping", month="2026-06", limit_amount=15000)
    ]

    # -----------------------
    # Demo Transactions
    # -----------------------
    transactions = [
        Transaction(
            amount=1200,
            category="Food",
            transaction_type="expense",
            date=date(2026, 6, 1)
        ),
        Transaction(
            amount=2500,
            category="Travel",
            transaction_type="expense",
            date=date(2026, 6, 5)
        ),
        Transaction(
            amount=10000,
            category="Salary",
            transaction_type="income",
            date=date(2026, 6, 10)
        )
    ]

    # -----------------------
    # Insert into DB
    # -----------------------
    db.session.add_all(budgets)
    db.session.add_all(transactions)

    db.session.commit()

print("Demo data seeded successfully.")
