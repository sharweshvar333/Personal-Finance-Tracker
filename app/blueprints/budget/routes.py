from flask import render_template
from . import budget_bp

@budget_bp.route("/budget")
def budget_home():
    return render_template("budget.html")
