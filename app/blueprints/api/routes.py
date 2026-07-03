from flask import jsonify, request, current_app
import time
from datetime import datetime

from . import api_bp
from models import Transaction
from app.extensions import db


@api_bp.route("/api/transactions", methods=["GET"])
def get_transactions():

    transactions = Transaction.query.all()

    data = []

    for t in transactions:
        data.append({
            "id": t.id,
            "amount": t.amount,
            "category": t.category,
            "transaction_type": t.transaction_type,
            "date": str(t.date)
        })

    return jsonify(data), 200


@api_bp.route("/api/transactions", methods=["POST"])
def create_transaction():

    data = request.get_json()

    transaction = Transaction(
        amount=data["amount"],
        category=data["category"],
        transaction_type=data["transaction_type"],
        date=datetime.strptime(
            data["date"],
            "%Y-%m-%d"
        ).date()
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "message": "Transaction added successfully"
    }), 201


@api_bp.route("/api/transactions/<int:id>", methods=["DELETE"])
def delete_transaction(id):

    transaction = Transaction.query.get(id)

    if not transaction:
        return jsonify({
            "error": "Transaction not found"
        }), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({
        "message": "Transaction deleted successfully"
    }), 200


@api_bp.route("/api/debug")
def debug():
    return jsonify({
        "database": current_app.config["SQLALCHEMY_DATABASE_URI"]
    })

@api_bp.route("/api/health")
def health_check():

    uptime = int(time.time() - current_app.config["START_TIME"])

    return {
        "status": "healthy",
        "message": "Personal Finance Tracker is running",
        "uptime_seconds": uptime
    }, 200