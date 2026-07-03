from database import SessionLocal
from models import Budget, Transaction
from datetime import date

session = SessionLocal()

budgets = [
    Budget(category="Food", month="2026-06", limit_amount=20000),
    Budget(category="Travel", month="2026-06", limit_amount=30000),
    Budget(category="Shopping", month="2026-06", limit_amount=15000)
]

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

session.add_all(budgets)
session.add_all(transactions)

session.commit()

print("Demo data seeded successfully.")

session.close()
