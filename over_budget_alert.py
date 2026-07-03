from database import SessionLocal
from models import Transaction, Budget

from sqlalchemy import func


session = SessionLocal()


budgets = session.query(Budget).all()


print("\nOVER BUDGET ALERTS")
print("=" * 60)


for budget in budgets:

    spent = (
        session.query(
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.category == budget.category
        )
        .filter(
            Transaction.transaction_type == "expense"
        )
        .scalar()
    )

    spent = spent or 0

    if spent > budget.limit_amount:

        excess = spent - budget.limit_amount

        print(
            f"🔴 {budget.category} OVER BUDGET by ₹{excess:.2f}"
        )

    else:

        remaining = budget.limit_amount - spent

        print(
            f"🟢 {budget.category} OK (₹{remaining:.2f} remaining)"
        )


session.close()
