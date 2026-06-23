from database import Session
from models import Transaction

session = Session()

transactions = session.query(
    Transaction
).all()

for txn in transactions:

    print(
        txn.id,
        txn.amount,
        txn.category,
        txn.transaction_type
    )

count = session.query(
    Transaction
).count()

print(f"Total Records: {count}")
