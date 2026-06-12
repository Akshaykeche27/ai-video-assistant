from flask import Flask, render_template
from flask_socketio import SocketIO
from datetime import timedelta

from config import Config
from app.extensions import db, bcrypt, jwt, migrate
from app.utils.auth import current_user, user_logged_in

socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)

    # Load Config
    app.config.from_object(Config)

    # JWT Configuration
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=2)
    app.config["JWT_COOKIE_SECURE"] = False  # True only in HTTPS production
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # SocketIO
    socketio.init_app(app)

    # Inject User into Templates
    @app.context_processor
    def inject_user():
        try:
            return {
                "current_user": current_user(),
                "is_logged_in": user_logged_in()
            }
        except Exception:
            return {
                "current_user": None,
                "is_logged_in": False
            }

    # Global Error Handler
    @app.errorhandler(Exception)
    def handle_all_error(error):
        app.logger.error(f"ERROR: {error}")
        return render_template(
            "error.html",
            error_message="An unexpected error occurred."
        ), 500

    # Register Blueprints
    from app.routes.home_route import home_bp
    from app.routes.video_route import video_bp
    from app.routes.auth.login_route import login_bp
    from app.routes.auth.register_route import register_bp
    from app.routes.auth.logout import logout_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(profile_bp)

    return app