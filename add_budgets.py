from database import SessionLocal
from models import Budget

session = SessionLocal()

food_budget = Budget(
    category="Food",
    month="2026-06",
    limit_amount=20000
)

travel_budget = Budget(
    category="Travel",
    month="2026-06",
    limit_amount=30000
)

shopping_budget = Budget(
    category="Shopping",
    month="2026-06",
    limit_amount=15000
)

session.add(food_budget)
session.add(travel_budget)
session.add(shopping_budget)

session.commit()

print("Budgets added successfully.")

session.close()
