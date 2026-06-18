import argparse
import time

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

def validate_input(func):

    def wrapper(*args, **kwargs):

        amount = args[0]

        if amount <= 0:

            print(
                "Error: Amount must be greater than 0"
            )

            return

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

expense_transaction = Transaction(
    1000,
    food.name,
    "expense"
)

income = 50000
expense = 10000

@validate_input
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

@validate_input
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

@timer
def show_report():

    print("------ Finance Report ------")

    print(f"Total Income  : ₹{income}")

    print(f"Total Expense : ₹{expense}")

    print(f"Balance       : ₹{income - expense}")

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

args = parser.parse_args()

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

    print("Income:", income)
    print("Expense:", expense)

    balance = income - expense

    print(
        "Current Balance:",
        balance
    )

elif args.command == "report":

    show_report()

else:

    parser.print_help()