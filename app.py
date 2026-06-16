import argparse

income = 50000
expense = 10000

parser = argparse.ArgumentParser(
    description="Personal Finance Tracker"
)

subparsers = parser.add_subparsers(dest="command")

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
    print(
        f"Expense Added: ₹{args.amount} | Category: {args.category}"
    )

elif args.command == "add-income":
    print(
        f"Income Added: ₹{args.amount} | Source: {args.source}"
    )

elif args.command == "balance":
    print("Income:", income)
    print("Expense:", expense)

    balance = income - expense
    print("Current Balance:", balance)

elif args.command == "report":
    print("------ Finance Report ------")
    print(f"Total Income  : ₹{income}")
    print(f"Total Expense : ₹{expense}")
    print(f"Balance       : ₹{income - expense}")
    
else:
    parser.print_help()
