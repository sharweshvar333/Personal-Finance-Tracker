from flask import render_template
from flask_login import login_required, current_user

from . import admin_bp
from models import User, Transaction, Budget, SavingsGoal
from app.extensions import db

from flask import render_template, redirect, url_for, flash


@admin_bp.route("/admin")
@login_required
def admin_dashboard():

    # Allow only admins
    if not current_user.is_admin:
        return "<h3>Access Denied</h3>", 403

    total_users = User.query.count()
    total_transactions = Transaction.query.count()
    total_budgets = Budget.query.count()
    total_goals = SavingsGoal.query.count()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_transactions=total_transactions,
        total_budgets=total_budgets,
        total_goals=total_goals
    )

@admin_bp.route("/admin/users")
@login_required
def manage_users():

    if not current_user.is_admin:
        return "<h3>Access Denied</h3>", 403

    users = User.query.order_by(User.id).all()

    return render_template(
        "admin_users.html",
        users=users
    )    

@admin_bp.route("/admin/users/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):

    if not current_user.is_admin:
        return "<h3>Access Denied</h3>", 403

    user = User.query.get_or_404(user_id)

    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("admin.manage_users"))

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")

    return redirect(url_for("admin.manage_users"))
