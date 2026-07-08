from flask import render_template, request, redirect, url_for, flash

from . import budget_bp

from app.extensions import db
from models import Budget, Transaction


@budget_bp.route("/budget", methods=["GET", "POST"])
def budget_home():

    if request.method == "POST":

        category = request.form.get("category")
        month = request.form.get("month")
        limit_amount = request.form.get("limit_amount")

        budget = Budget(
            category=category,
            month=month,
            limit_amount=float(limit_amount)
        )

        db.session.add(budget)
        db.session.commit()

        flash("Budget created successfully!", "success")

        return redirect(url_for("budget.budget_home"))

    budgets = Budget.query.order_by(Budget.month.desc()).all()

    # Data for Chart.js
    budget_labels = []
    budget_limits = []
    budget_spent = []

    for budget in budgets:

        spent = db.session.query(
            db.func.sum(Transaction.amount)
        ).filter(
            Transaction.category == budget.category,
            Transaction.transaction_type == "expense"
        ).scalar()

        budget.spent = spent or 0

        budget.remaining = budget.limit_amount - budget.spent

        if budget.limit_amount > 0:
            budget.percent = min(
                (budget.spent / budget.limit_amount) * 100,
                100
            )
        else:
            budget.percent = 0

        budget.status = (
            "Exceeded"
            if budget.remaining < 0
            else "Within Budget"
        )

        # Chart data
        budget_labels.append(budget.category)
        budget_limits.append(budget.limit_amount)
        budget_spent.append(budget.spent)

    return render_template(
        "budget.html",
        budgets=budgets,
        budget_labels=budget_labels,
        budget_limits=budget_limits,
        budget_spent=budget_spent
    )
    