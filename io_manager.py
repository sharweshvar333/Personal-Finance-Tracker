import csv
import json
import logging


def save_transaction(transaction):
    with open(
        "transactions.csv",
        "a",
        newline=""
    ) as file:

        fieldnames = [
            "amount",
            "category",
            "type"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(
            {
                "amount": transaction.amount,
                "category": transaction.category,
                "type": transaction.transaction_type
            }
        )


def import_csv():

    transactions = []

    try:

        with open(
            "transactions.csv",
            "r"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                transactions.append(row)

    except FileNotFoundError:

        print(
            "No transactions.csv file found."
        )

    return transactions


def export_json():

    transactions = []

    try:

        with open(
            "transactions.csv",
            "r"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                transactions.append(row)

        with open(
            "transactions.json",
            "w"
        ) as json_file:

            json.dump(
                transactions,
                json_file,
                indent=4
            )

        print(
            "Exported successfully to transactions.json"
        )

    except FileNotFoundError:

        print(
            "No transactions.csv file found."
        )


def calculate_totals():

    total_income = 0
    total_expense = 0

    try:

        with open(
            "transactions.csv",
            "r"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                amount = float(
                    row["amount"]
                )

                if row["type"] == "income":
                    total_income += amount

                elif row["type"] == "expense":
                    total_expense += amount

    except FileNotFoundError:
        pass

    return total_income, total_expense


def bulk_import(
    file_path,
    add_income,
    add_expense
):

    imported = 0
    failed = 0

    try:

        with open(
            file_path,
            "r"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                try:

                    amount = float(
                        row["amount"]
                    )

                    category = row["category"]

                    transaction_type = row["type"]

                    if transaction_type == "expense":

                        add_expense(
                            amount,
                            category
                        )

                    elif transaction_type == "income":

                        add_income(
                            amount,
                            category
                        )

                    else:

                        raise ValueError(
                            f"Invalid transaction type: {transaction_type}"
                        )

                    imported += 1

                except Exception as e:

                    logging.error(
                        f"Failed row {row}: {e}"
                    )

                    failed += 1

        print(
            f"\nImported: {imported}"
        )

        print(
            f"Failed: {failed}"
        )

    except FileNotFoundError:

        print(
            f"File not found: {file_path}"
        )