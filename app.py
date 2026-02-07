from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from models import db, User, Note
from utils import md_to_html

app = Flask(__name__)
app.secret_key = "dev-secret-key" # TODO: os.environ.get()にする
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # 既存ユーザー確認
        if User.query.filter_by(username=username).first():
            flash("そのユーザー名はすでに使われています。", "danger")
            return redirect(url_for("register"))

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("ユーザー登録が完了しました。", "success")
        return redirect("/notes") # ノート一覧へ

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("ログインしました。", "success")

            next_page = request.form.get("next")
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("notes_index")

            return redirect(next_page)
        else:
            flash("ユーザー名またはパスワードが違います。", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "info")
    return redirect("/login")


@app.route("/notes/new")
@login_required
def new_note():
    return render_template("notes/new.html")


@app.route("/notes", methods=["POST"])
@login_required
def create_note():
    user_id = current_user.id
    title = request.form["title"]
    content_md = request.form["content_md"]

    note = Note(user_id=user_id, title=title, content_md=content_md)
    db.session.add(note)
    db.session.commit()

    html_text = md_to_html(note.content_md)

    flash("ノートを作成しました。", "success")

    return render_template("notes/created.html", note=note, html_text=html_text)


@app.route("/notes")
@login_required
def notes_index():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
    return render_template("notes/index.html", notes=notes)


@app.route("/notes/<int:note_id>")
@login_required
def show_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()
    html_text = md_to_html(note.content_md)
    return render_template("notes/show.html", note=note, html_text=html_text)


@app.route("/notes/<int:note_id>/edit")
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()
    return render_template("notes/edit.html", note=note)


@app.route("/notes/<int:note_id>/update", methods=["POST"])
@login_required
def update_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    note.title = request.form["title"]
    note.content_md = request.form["content_md"]

    db.session.commit()

    flash("ノートを更新しました。", "info")

    return redirect(f"/notes/{note.id}")


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(note)
    db.session.commit()

    flash("ノートを削除しました。", "danger")

    return redirect("/notes")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
