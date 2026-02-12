from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import os

from .models import db, User
from .auth import auth_bp
from .notes import notes_bp

migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "fallback-secret"),
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///notes.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    return app