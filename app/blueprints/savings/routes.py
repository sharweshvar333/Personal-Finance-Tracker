from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from . import savings_bp

from app.extensions import db
from app.forms import SavingsGoalForm, DepositForm
from models import SavingsGoal


@savings_bp.route("/goals", methods=["GET", "POST"])
@login_required
def goals():

    form = SavingsGoalForm()

    if form.validate_on_submit():

        goal = SavingsGoal(
            name=form.goal_name.data,
            target_amount=float(form.target_amount.data),
            current_amount=float(form.current_amount.data),
            deadline=form.target_date.data
        )

        db.session.add(goal)
        db.session.commit()

        flash("Savings Goal created successfully!", "success")

        return redirect(url_for("savings.goals"))

    goals = SavingsGoal.query.all()

    total_goals = len(goals)
    completed_goals = sum(
        1 for goal in goals if goal.completed
    )

    total_saved = sum(
        goal.current_amount
        for goal in goals
    )

    total_target = sum(
        goal.target_amount
        for goal in goals
    )

    remaining = total_target - total_saved

    return render_template(
        "goals.html",
        form=form,
        goals=goals,
        total_goals=total_goals,
        completed_goals=completed_goals,
        total_saved=total_saved,
        remaining=remaining
    )


@savings_bp.route("/deposit/<int:goal_id>", methods=["GET", "POST"])
@login_required
def deposit(goal_id):

    goal = SavingsGoal.query.get_or_404(goal_id)

    form = DepositForm()

    if form.validate_on_submit():

        goal.current_amount += float(form.amount.data)

        # Mark goal as completed if target reached
        if goal.current_amount >= goal.target_amount:
            goal.completed = True

        db.session.commit()

        flash("Money added successfully!", "success")

        return redirect(url_for("savings.goals"))

    return render_template(
        "deposit.html",
        form=form,
        goal=goal
    )
    
@savings_bp.route("/delete/<int:goal_id>", methods=["POST"])
@login_required
def delete_goal(goal_id):

    goal = SavingsGoal.query.get_or_404(goal_id)

    db.session.delete(goal)
    db.session.commit()

    flash("Savings goal deleted successfully!", "success")

    return redirect(url_for("savings.goals"))