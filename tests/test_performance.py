import time
from datetime import date

from models import Transaction
from app.extensions import db


def test_insert_100_transactions(app):
    with app.app_context():

        start = time.time()

        for _ in range(100):
            transaction = Transaction(
                amount=100,
                category="Food",
                transaction_type="expense",
                date=date.today()      # ✅ Correct
            )

            db.session.add(transaction)

        db.session.commit()

        end = time.time()

        assert (end - start) < 5
        