from database import SessionLocal
from models import Budget, Transaction
from sqlalchemy import func

session = SessionLocal()

budgets = session.query(Budget).all()

print("\nBUDGET REPORT")
print("=" * 60)

for budget in budgets:

    spent = (
        session.query(
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.category == budget.category,
            Transaction.transaction_type == "expense"
        )
        .scalar()
    )

    if spent is None:
        spent = 0

    remaining = budget.limit_amount - spent

    print(f"\nCategory : {budget.category}")
    print(f"Month    : {budget.month}")
    print(f"Budget   : ₹{budget.limit_amount:.2f}")
    print(f"Spent    : ₹{spent:.2f}")

    if remaining < 0:
        print(
            f"ALERT: OVER BUDGET by ₹{abs(remaining):.2f}"
        )
    else:
        print(
            f"Remaining: ₹{remaining:.2f}"
        )

session.close()
