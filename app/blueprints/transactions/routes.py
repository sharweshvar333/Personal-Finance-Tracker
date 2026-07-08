import csv
from io import StringIO
from flask import make_response
from app.extensions import limiter
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session
)

from . import transactions_bp

from flask_login import login_required

from app.forms import TransactionForm
from app.extensions import db

from app.extensions import db
from models import Transaction

import pandas as pd
from datetime import date

from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from reportlab.lib import colors

from flask import send_file

import time
from app.performance import log_slow_query


@transactions_bp.route("/transactions", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute", methods=["POST"])
def transactions_home():

    form = TransactionForm()

    # Add Transaction
    if form.validate_on_submit():

        transaction = Transaction(
            amount=form.amount.data,
            category=form.category.data,
            transaction_type=form.transaction_type.data,
            date=form.date.data,

            is_recurring=form.is_recurring.data,
            recurrence=form.recurrence.data if form.is_recurring.data else None,
            start_date=form.start_date.data if form.is_recurring.data else None,
            end_date=form.end_date.data if form.is_recurring.data else None,
            last_processed=form.start_date.data if form.is_recurring.data else None
        )

        db.session.add(transaction)
        db.session.commit()

        flash("Transaction added successfully!", "success")

        return redirect(url_for("transactions.transactions_home"))

    # ----------------------------
    # Filters
    # ----------------------------

    category = request.args.get("category")
    search = request.args.get("search")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    query = Transaction.query
    if search:
        query = query.filter(
             Transaction.category.ilike(f"%{search}%")
        )

    # Filter by category
    if category:
        query = query.filter(
            Transaction.category == category
        )

    # Filter by start date
    if start_date:
        query = query.filter(
            Transaction.date >= start_date
        )

    # Filter by end date
    if end_date:
        query = query.filter(
            Transaction.date <= end_date
        )

    # ----------------------------
    # Pagination
    # ----------------------------

    page = request.args.get("page", 1, type=int)

    start = time.perf_counter()

    transactions = query.order_by(
        Transaction.date.desc()
    ).paginate(
        page=page,
        per_page=5
    )

    elapsed = time.perf_counter() - start
    log_slow_query("Load Transactions Page", elapsed)

    return render_template(
        "transactions.html",
        form=form,
        transactions=transactions,
        search=search
    )



@transactions_bp.route("/dashboard")
@login_required
def dashboard():

    print("===== Dashboard route called =====")

    start = time.perf_counter()

    transactions = Transaction.query.all()

    elapsed = time.perf_counter() - start 
    log_slow_query("Dashboard Query", elapsed)

    category_totals = {}

    for transaction in transactions:
        if transaction.transaction_type.lower() == "expense":
            category = transaction.category
            category_totals[category] = (
                category_totals.get(category, 0)
                + transaction.amount
            )

    monthly_totals = {}

    for transaction in transactions:
        if transaction.transaction_type.lower() == "expense":
            month = transaction.date.strftime("%b %Y")
            monthly_totals[month] = (
                monthly_totals.get(month, 0)
                + transaction.amount
            )

    print(category_totals)
    print(monthly_totals)

    return render_template(
        "dashboard.html",
        category_labels=list(category_totals.keys()),
        category_values=list(category_totals.values()),
        month_labels=list(monthly_totals.keys()),
        month_values=list(monthly_totals.values())
    )


@transactions_bp.route("/import", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute", methods=["POST"])
def import_transactions():

    if request.method == "POST":

        # User clicked Confirm Import
        if "confirm_import" in request.form:

            rows = session.get("csv_rows", [])

            count = 0

            for row in rows:

                transaction = Transaction(
                    amount=float(row["amount"]),
                    category=row["category"],
                    transaction_type=row["type"],
                    date=date.today()
                )

                db.session.add(transaction)
                count += 1

            db.session.commit()

            session.pop("csv_rows", None)

            flash(f"{count} transactions imported successfully!", "success")

            return redirect(url_for("transactions.transactions_home"))

        # User uploaded CSV
        file = request.files["csv_file"]

        df = pd.read_csv(file)

        # Store all rows temporarily
        session["csv_rows"] = df.to_dict(orient="records")

        preview = df.head().to_html(
            classes="table table-bordered table-striped table-hover align-middle text-center",
            index=False,
            border=0
        )

        return render_template(
            "import.html",
            preview=preview
        )

    return render_template("import.html")

    
@transactions_bp.route("/export")
@login_required
def export_transactions():

    start = time.perf_counter()
    transactions = Transaction.query.all()
    elapsed = time.perf_counter() - start
    log_slow_query("Export CSV Query", elapsed)

    output = StringIO()

    writer = csv.writer(output)

    # CSV Header
    writer.writerow([
        "Amount",
        "Category",
        "Transaction Type",
        "Date"
    ])

    # CSV Data
    for transaction in transactions:

        writer.writerow([
            transaction.amount,
            transaction.category,
            transaction.transaction_type,
            transaction.date
        ])

    response = make_response(output.getvalue())

    response.headers["Content-Disposition"] = \
        "attachment; filename=transactions.csv"

    response.headers["Content-type"] = "text/csv"

    return response

@transactions_bp.route("/export/pdf")
@login_required
def export_pdf():

    start = time.perf_counter()
    transactions = Transaction.query.all()
    elapsed = time.perf_counter() - start
    log_slow_query("Export PDF Query", elapsed)
    
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    data = [
        ["Amount", "Category", "Type", "Date"]
    ]

    for transaction in transactions:
        data.append([
            str(transaction.amount),
            transaction.category,
            transaction.transaction_type,
            str(transaction.date)
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige)
    ]))

    doc.build([table])

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="transactions_report.pdf",
        mimetype="application/pdf"
    )
