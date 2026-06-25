from app.extensions import db


class Transaction(db.Model):

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float)

    category = db.Column(db.String)

    transaction_type = db.Column(db.String)

    date = db.Column(db.Date, nullable=False)


class Budget(db.Model):

    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)

    category = db.Column(db.String, nullable=False)

    month = db.Column(db.String, nullable=False)

    limit_amount = db.Column(db.Float, nullable=False)
    