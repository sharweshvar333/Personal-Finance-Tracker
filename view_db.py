from app import create_app
from models import Transaction

app = create_app()

with app.app_context():
    transactions = Transaction.query.all()

    for transaction in transactions:
        print(
            transaction.id,
            transaction.amount,
            transaction.category,
            transaction.transaction_type,
            transaction.date
        )

    print(f"\nTotal Records: {len(transactions)}")
    