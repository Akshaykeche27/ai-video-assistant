from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User
from functools import wraps
from flask import redirect, flash


from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User
from functools import wraps
from flask import redirect, flash

def current_user():
    try:
        verify_jwt_in_request(optional=True)

        user_id = get_jwt_identity()

        if not user_id:
            return None

        return User.query.get(int(user_id))

    except Exception:
        return None


def user_logged_in():
    return current_user() is not None


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        user = current_user()

        if not user:
            flash("Please login first", "error")
            return redirect("/login")

        return f(*args, **kwargs)

    return wrapper


def user_logged_in():
    try:
        verify_jwt_in_request()
        return True
    except Exception:
        return False