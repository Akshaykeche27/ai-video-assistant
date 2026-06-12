


from flask import Blueprint,render_template,request,redirect,url_for,flash,make_response
# from app import db
from app.models.user import User

from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from app.extensions import bcrypt

from app.utils.auth import current_user


login_bp=Blueprint("login",__name__)

@login_bp.route("/login",methods=["GET","POST"])
def login():
    user=current_user()
    if user:
        return redirect('/home')
    if request.method=="POST":
        
        email=request.form.get("email")
        user=User.query.filter_by(email=email).first()
        if not user:
            flash("INVALID USER","error")
            return redirect('/login')
        
        password=request.form.get("password")
        is_valid=bcrypt.check_password_hash(user.password,password)

        if  not is_valid:
            flash("Invalid User",'error')
            return redirect('/login')
        


        access_token=create_access_token(identity=str(user.id))
        responce=make_response(redirect('/'))
        set_access_cookies(responce,access_token)

        flash("Login Successful","success")
        
        
        return responce
    return render_template("login.html")   