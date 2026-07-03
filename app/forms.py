from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    SelectField,
    DateField,
    SubmitField,
    StringField,
    PasswordField
)

from wtforms.validators import (
    DataRequired,
    NumberRange,
    Length
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
    