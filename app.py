from flask import Flask, render_template
from flask_login import LoginManager, login_required

from models import db, User
from auth import auth_bp
from notes import notes_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key" # TODO: os.environ.get()にする
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    return app

app = create_app()

@app.route("/")
@login_required
def index():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
