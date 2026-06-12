from flask import Blueprint,flash
from flask import redirect

from flask_jwt_extended import unset_access_cookies

logout_bp=Blueprint("logout",__name__)

@logout_bp.route("/logout")

def logout():
    responce=redirect("/login")
   
    unset_access_cookies(responce)
    flash("user loggout Successful","error")
    return responce
