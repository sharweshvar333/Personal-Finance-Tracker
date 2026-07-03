import argparse
import time
import logging

from io_manager import (
    save_transaction,
    import_csv,
    export_json,
    calculate_totals,
    bulk_import
)


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class TransactionError(Exception):
    pass


class InvalidAmountError(TransactionError):
    pass


class InvalidCategoryError(TransactionError):
    pass


class BudgetExceededError(TransactionError):
    pass


def timer(func):

    def wrapper(*args, **kwargs):

        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        print(
            f"\nExecution Time: {end - start:.4f} seconds"
        )

        return result

    return wrapper


def validate_expense(func):

    def wrapper(*args, **kwargs):

        amount = args[0]
        category = args[1]

        VALID_CATEGORIES = [
            "Food",
            "Travel",
            "Shopping"
        ]

        if amount <= 0:
            raise InvalidAmountError(
                "Amount must be greater than 0"
            )

        if category not in VALID_CATEGORIES:
            raise InvalidCategoryError(
                f"Invalid category: {category}"
            )

        if category == "Food" and amount > 5000:
            raise BudgetExceededError(
                "Food budget exceeded"
            )

        return func(*args, **kwargs)

    return wrapper


def validate_income(func):

    def wrapper(*args, **kwargs):

        amount = args[0]

        if amount <= 0:
            raise InvalidAmountError(
                "Amount must be greater than 0"
            )

        return func(*args, **kwargs)

    return wrapper


class Category:

    def __init__(self, name):
        self.name = name


class Budget:

    def __init__(self, category, limit):
        self.category = category
        self.limit = limit


class Transaction:

    def __init__(
        self,
        amount,
        category,
        transaction_type
    ):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type

    def display(self):

        print(
            f"{self.transaction_type}: ₹{self.amount} ({self.category})"
        )


food = Category("Food")

food_budget = Budget(
    food.name,
    5000
)


@validate_expense
def add_expense(
    amount,
    category
):

    expense = Transaction(
        amount,
        category,
        "expense"
    )

    expense.display()

    save_transaction(expense)

    logging.info(
        f"Expense Added: {amount} - {category}"
    )


@validate_income
def add_income(
    amount,
    source
):

    income = Transaction(
        amount,
        source,
        "income"
    )

    income.display()

    save_transaction(income)

    logging.info(
        f"Income Added: {amount} - {source}"
    )


@timer
def show_report():

    income, expense = calculate_totals()

    print(
        "------ Finance Report ------"
    )

    print(
        f"Total Income  : ₹{income}"
    )

    print(
        f"Total Expense : ₹{expense}"
    )

    print(
        f"Balance       : ₹{income - expense}"
    )


parser = argparse.ArgumentParser(
    description="Personal Finance Tracker"
)

subparsers = parser.add_subparsers(
    dest="command"
)


expense_parser = subparsers.add_parser(
    "add-expense",
    help="Add a new expense"
)

expense_parser.add_argument(
    "--amount",
    type=float,
    required=True,
    help="Expense amount"
)

expense_parser.add_argument(
    "--category",
    required=True,
    help="Expense category"
)


income_parser = subparsers.add_parser(
    "add-income",
    help="Add new income"
)

income_parser.add_argument(
    "--amount",
    type=float,
    required=True
)

income_parser.add_argument(
    "--source",
    required=True
)


subparsers.add_parser(
    "balance",
    help="Show current balance"
)

subparsers.add_parser(
    "report",
    help="Show finance report"
)

subparsers.add_parser(
    "import-csv",
    help="View all transactions"
)

subparsers.add_parser(
    "export-json",
    help="Export CSV data to JSON"
)

bulk_parser = subparsers.add_parser(
    "bulk-import",
    help="Bulk import transactions from CSV"
)

bulk_parser.add_argument(
    "--file",
    required=True,
    help="CSV file path"
)

def main():

    args = parser.parse_args()

    try:

        if args.command == "add-expense":

            add_expense(
                args.amount,
                args.category
            )

        elif args.command == "add-income":

            add_income(
                args.amount,
                args.source
            )

        elif args.command == "balance":

            income, expense = calculate_totals()

            print(
                f"Income: ₹{income}"
            )

            print(
                f"Expense: ₹{expense}"
            )

            print(
                f"Current Balance: ₹{income - expense}"
            )

        elif args.command == "report":

            show_report()

        elif args.command == "import-csv":

            transactions = import_csv()

            for transaction in transactions:
                print(transaction)

        elif args.command == "export-json":

            export_json()

        elif args.command == "bulk-import":

            bulk_import(
                args.file,
                add_income,
                add_expense
            )    

        else:

            parser.print_help()

    except TransactionError as e:

        logging.error(str(e))

        print(
            f"Transaction Error: {e}"
        )


if __name__ == "__main__":
    main()
