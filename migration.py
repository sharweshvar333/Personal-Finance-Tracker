import csv

from database import Session
from models import Transaction
from datetime import date


session = Session()

with open(
    "data/transactions.csv",
    "r"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        transaction = Transaction(
             amount=float(row["amount"]),
             category=row["category"],
             transaction_type=row["type"],
             date=date.today()
        )

        session.add(transaction)

session.commit()

print("CSV data migrated successfully.")
