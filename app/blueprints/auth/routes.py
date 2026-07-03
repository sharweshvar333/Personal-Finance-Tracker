from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

from . import auth_bp
from models import User
from app.extensions import db
from app.forms import LoginForm, RegisterForm


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(
            username=form.username.data
        ).first()

        if existing_user:
            flash("Username already exists.", "danger")
            return redirect(url_for("auth.register"))

        new_user = User(
            username=form.username.data,
            password_hash=generate_password_hash(
                form.password.data
            )
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/register.html",
        form=form
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if user and check_password_hash(
            user.password_hash,
            form.password.data
        ):

            login_user(user)

            flash("Welcome back!", "success")

            return redirect(url_for("home"))

        flash("Invalid username or password.", "danger")

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/login.html",
        form=form
    )


@auth_bp.route("/logout")
def logout():

    logout_user()

    flash("Logged out successfully.", "info")

    return redirect(url_for("auth.login"))
