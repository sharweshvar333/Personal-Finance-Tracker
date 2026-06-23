import csv

from database import Session
from models import Transaction


def verify_migration():

    csv_count = 0
    csv_total = 0

    with open(
        "data/transactions.csv",
        "r"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            csv_count += 1

            csv_total += float(
                row["amount"]
            )

    session = Session()

    db_count = session.query(
        Transaction
    ).count()

    db_total = sum(
        transaction.amount
        for transaction in session.query(
            Transaction
        ).all()
    )

    print("\n===== Migration Verification =====")

    print(
        f"CSV Rows      : {csv_count}"
    )

    print(
        f"Database Rows : {db_count}"
    )

    print(
        f"CSV Total Amount      : ₹{csv_total}"
    )

    print(
        f"Database Total Amount : ₹{db_total}"
    )

    if csv_count == db_count:

        print(
            "\n✓ Row Count Verification PASSED"
        )

    else:

        print(
            "\n✗ Row Count Verification FAILED"
        )

    if csv_total == db_total:

        print(
            "✓ Amount Verification PASSED"
        )

    else:

        print(
            "✗ Amount Verification FAILED"
        )

    session.close()


if __name__ == "__main__":
    verify_migration()
    