from flask import Flask,render_template,redirect,Blueprint
home_bp=Blueprint("home",__name__)
from app.utils.auth import current_user
@home_bp.route("/")
def home():
    return render_template("index.html")


