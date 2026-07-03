from database import SessionLocal
from models import Budget

session = SessionLocal()

session.query(Budget).delete()
session.commit()

print("All budgets deleted.")

session.close()
