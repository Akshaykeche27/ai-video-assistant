from flask import Flask,render_template,redirect,Blueprint
register_bp=Blueprint("register",__name__)

@register_bp.route("/register")
def register():
    return render_template("register.html")
