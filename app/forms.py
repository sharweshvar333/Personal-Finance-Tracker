from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    SelectField,
    DateField,
    SubmitField,
    StringField,
    PasswordField,
    DecimalField,
    BooleanField
)

from wtforms.validators import (
    DataRequired,
    NumberRange,
    Length,
    Optional
)


class TransactionForm(FlaskForm):

    amount = FloatField(
        "Amount",
        validators=[
            DataRequired(),
            NumberRange(min=0.01)
        ]
    )

    category = SelectField(
        "Category",
        choices=[
            ("Food", "Food"),
            ("Travel", "Travel"),
            ("Shopping", "Shopping"),
            ("Salary", "Salary"),
            ("Freelance", "Freelance")
        ],
        validators=[DataRequired()]
    )

    transaction_type = SelectField(
        "Transaction Type",
        choices=[
            ("income", "Income"),
            ("expense", "Expense")
        ],
        validators=[DataRequired()]
    )

    date = DateField(
        "Date",
        validators=[DataRequired()]
    )

    # ----------------------------
    # NEW FIELDS
    # ----------------------------

    is_recurring = BooleanField(
        "Recurring Transaction"
    )

    recurrence = SelectField(
        "Repeat",
        choices=[
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly")
        ],
        validators=[Optional()]
    )

    start_date = DateField(
        "Start Date",
        validators=[Optional()]
    )

    end_date = DateField(
        "End Date",
        validators=[Optional()]
    )

    submit = SubmitField("Add Transaction")


class LoginForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Login")


class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    submit = SubmitField("Register")


class SavingsGoalForm(FlaskForm):

    goal_name = StringField(
        "Goal Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    target_amount = DecimalField(
        "Target Amount",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    current_amount = DecimalField(
        "Current Amount",
        default=0
    )

    target_date = DateField(
        "Target Date",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Create Goal")


class DepositForm(FlaskForm):

    amount = FloatField(
        "Deposit Amount",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    submit = SubmitField("Deposit")
    