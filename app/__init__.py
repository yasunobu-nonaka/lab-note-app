from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from .models import db, User
from .auth import auth_bp
from .notes import notes_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key" # TODO: os.environ.get()にする
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    migrate.init_app(app, db)
    # Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    return app