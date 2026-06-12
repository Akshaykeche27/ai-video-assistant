from flask import Flask,render_template,redirect,Blueprint
profile_bp=Blueprint("profile",__name__)
from app.utils.auth import login_required


@profile_bp.route("/profile")
@login_required

def profile():
    return render_template("profile.html")
