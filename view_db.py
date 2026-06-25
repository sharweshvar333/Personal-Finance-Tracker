from database import SessionLocal
from models import Transaction

session = SessionLocal()

transactions = session.query(Transaction).all()

for transaction in transactions:
    print(
        transaction.id,
        transaction.amount,
        transaction.category,
        transaction.transaction_type,
        transaction.date
    )

print(f"\nTotal Records: {len(transactions)}")

session.close()
