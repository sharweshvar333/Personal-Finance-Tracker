import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from app import Category
from app import Budget
from app import Transaction

def test_category_food():
    category = Category("Food")
    assert category.name == "Food"


def test_category_travel():
    category = Category("Travel")
    assert category.name == "Travel"


def test_category_shopping():
    category = Category("Shopping")
    assert category.name == "Shopping"


def test_category_name_is_string():
    category = Category("Food")
    assert isinstance(category.name, str)


def test_category_not_none():
    category = Category("Food")
    assert category.name is not None


def test_budget_category():
    budget = Budget("Food", 5000)
    assert budget.category == "Food"


def test_budget_limit():
    budget = Budget("Food", 5000)
    assert budget.limit == 5000


def test_budget_limit_is_int():
    budget = Budget("Food", 5000)
    assert isinstance(budget.limit, int)


def test_budget_limit_positive():
    budget = Budget("Food", 5000)
    assert budget.limit > 0


def test_budget_category_is_string():
    budget = Budget("Food", 5000)
    assert isinstance(budget.category, str)


def test_transaction_amount():
    transaction = Transaction(
        1000,
        "Food",
        "expense"
    )
    assert transaction.amount == 1000


def test_transaction_category():
    transaction = Transaction(
        1000,
        "Food",
        "expense"
    )
    assert transaction.category == "Food"


def test_transaction_type():
    transaction = Transaction(
        1000,
        "Food",
        "expense"
    )
    assert transaction.transaction_type == "expense"


def test_transaction_amount_positive():
    transaction = Transaction(
        1000,
        "Food",
        "expense"
    )
    assert transaction.amount > 0


def test_income_transaction():
    transaction = Transaction(
        50000,
        "Salary",
        "income"
    )
    assert transaction.transaction_type == "income"