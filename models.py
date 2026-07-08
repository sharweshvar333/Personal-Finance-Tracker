from app.extensions import db
from flask_login import UserMixin


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float, nullable=False)
    category = db.Column(
        db.String(100),
        index=True
    )
    transaction_type = db.Column(
        db.String(20),
        index=True
    )
    date = db.Column(
        db.Date,
        index=True
    )

    # -------- Recurring Transaction Fields --------
    is_recurring = db.Column(db.Boolean, default=False)

    recurrence = db.Column(
        db.String(20)
    )  # daily / weekly / monthly

    start_date = db.Column(db.Date)

    end_date = db.Column(db.Date)

    last_processed = db.Column(db.Date)


class Budget(db.Model):
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    month = db.Column(db.String, nullable=False)
    limit_amount = db.Column(db.Float, nullable=False)


class SavingsGoal(db.Model):
    __tablename__ = "savings_goals"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    target_amount = db.Column(db.Float, nullable=False)

    current_amount = db.Column(
        db.Float,
        default=0
    )

    deadline = db.Column(db.Date)

    completed = db.Column(
        db.Boolean,
        default=False
    )


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    