from database import SessionLocal
from models import Budget

session = SessionLocal()

budgets = session.query(Budget).all()

for budget in budgets:
    print(
        budget.id,
        budget.category,
        budget.month,
        budget.limit_amount
    )

session.close()
