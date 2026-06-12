import uuid
import bcrypt

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response
)

from flask_jwt_extended import (
    create_access_token,
    set_access_cookies
)

from app import db
from app.models.user import User
from app.utils.auth import current_user


register_bp = Blueprint("register", __name__)


@register_bp.route("/register", methods=["GET", "POST"])
def register():

    user = current_user()

    if user:
        return redirect("/home")

    if request.method == "POST":

        try:

            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password")
            profession = request.form.get("profession", "").strip()
            purpose = request.form.get("purpose", "").strip()
            age = request.form.get("age")

            # =========================
            # Validation
            # =========================

            if not username:
                flash("Username is required", "error")
                return redirect("/register")

            if not email:
                flash("Email is required", "error")
                return redirect("/register")

            if not password:
                flash("Password is required", "error")
                return redirect("/register")

            if not age:
                flash("Age is required", "error")
                return redirect("/register")

            age = int(age)

            # =========================
            # Existing User Check
            # =========================

            existing_user = User.query.filter_by(
                email=email
            ).first()

            if existing_user:
                flash("User already exists", "error")
                return redirect("/register")

            # =========================
            # Password Hashing
            # =========================

            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            # =========================
            # Create User
            # =========================

            new_user = User(
                uuid=str(uuid.uuid4()),
                username=username,
                email=email,
                password=hashed_password,
                profession=profession,
                age=age,
                purpose=purpose
            )

            db.session.add(new_user)
            db.session.commit()

            # =========================
            # Login User
            # =========================

            access_token = create_access_token(
                identity=str(new_user.id)
            )

            response = make_response(
                redirect(url_for("home.home"))
            )

            set_access_cookies(
                response,
                access_token
            )

            flash(
                "Account created successfully",
                "success"
            )

            return response

        except Exception as e:

            db.session.rollback()

            print("\nREGISTER ERROR")
            print(e)
            print("\n")

            flash(
                "Registration failed. Check terminal.",
                "error"
            )

            return redirect("/register")

    return render_template("register.html")