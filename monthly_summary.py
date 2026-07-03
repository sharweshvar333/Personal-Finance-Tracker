from database import SessionLocal
from models import Transaction
from sqlalchemy import func

session = SessionLocal()

results = (
    session.query(
        func.strftime(
            "%Y-%m",
            Transaction.date
        ).label("month"),

        Transaction.category,

        func.sum(
            Transaction.amount
        ).label("total_spent")
    )
    .filter(
        Transaction.transaction_type == "expense"
    )
    .group_by(
        "month",
        Transaction.category
    )
    .order_by(
        "month",
        func.sum(Transaction.amount).desc()
    )
    .all()
)

monthly_summary = {}

for month, category, total in results:

    if month not in monthly_summary:
        monthly_summary[month] = []

    monthly_summary[month].append(
        (category, total)
    )

print("\nTOP 3 CATEGORIES BY SPENDING")
print("=" * 40)

for month, categories in monthly_summary.items():

    print(f"\nMonth: {month}")
    print("-" * 30)

    for category, total in categories[:3]:

        print(
            f"{category:<12} ₹{total:.2f}"
        )

session.close()