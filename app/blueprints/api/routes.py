from flask import jsonify, request, current_app
import time
from datetime import datetime

from . import api_bp
from models import Transaction
from app.extensions import db
from app.extensions import csrf

csrf.exempt(api_bp)

@api_bp.route("/api/v1/transactions", methods=["GET"])
def get_transactions():
    """
    Get all transactions
    ---
    tags:
      - Transactions

    responses:
      200:
        description: Returns all transactions

        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1

              amount:
                type: number
                example: 500.0

              category:
                type: string
                example: Food

              transaction_type:
                type: string
                example: expense

              date:
                type: string
                example: "2026-07-06"
    """

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


@api_bp.route("/api/v1/transactions", methods=["POST"])
def create_transaction():
    """
    Create a new transaction
    ---
    tags:
      - Transactions

    parameters:
      - in: body
        name: body
        required: true

        schema:
          type: object

          required:
            - amount
            - category
            - transaction_type
            - date

          properties:

            amount:
              type: number
              example: 750

            category:
              type: string
              example: Shopping

            transaction_type:
              type: string
              example: expense

            date:
              type: string
              example: "2026-07-06"

    responses:
      201:
        description: Transaction created successfully
    """

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


@api_bp.route("/api/v1/transactions/<int:id>", methods=["DELETE"])
def delete_transaction(id):
    """
    Delete a transaction
    ---
    tags:
      - Transactions

    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1

    responses:
      200:
        description: Transaction deleted successfully

      404:
        description: Transaction not found
    """

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


@api_bp.route("/api/v1/debug")
def debug():
    """
    Debug database configuration
    ---
    tags:
      - Debug

    responses:
      200:
        description: Database URI
    """

    return jsonify({
        "database": current_app.config["SQLALCHEMY_DATABASE_URI"]
    })


@api_bp.route("/api/v1/health")
def health_check():
    """
    Health Check
    ---
    tags:
      - System

    responses:
      200:
        description: Application health status
    """

    uptime = int(time.time() - current_app.config["START_TIME"])

    return {
        "status": "healthy",
        "message": "Personal Finance Tracker is running",
        "uptime_seconds": uptime
    }, 200
