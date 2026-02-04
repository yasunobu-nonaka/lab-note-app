from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user
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
def index():
    return render_template("index.html")


@app.route("/register")
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
        return redirect(url_for("notes")) # ノート一覧へ

    return render_template("register.html")


@app.route("/notes/new")
def new_note():
    return render_template("notes/new.html")


@app.route("/notes", methods=["POST"])
def create_note():
    title = request.form["title"]
    content_md = request.form["content_md"]

    note = Note(title=title, content_md=content_md)
    db.session.add(note)
    db.session.commit()

    html_text = md_to_html(note.content_md)

    flash("ノートを作成しました。", "success")

    return render_template("notes/created.html", note=note, html_text=html_text)


@app.route("/notes")
def notes_index():
    notes = Note.query.order_by(Note.id.desc()).all()
    return render_template("notes/index.html", notes=notes)


@app.route("/notes/<int:note_id>")
def show_note(note_id):
    note = Note.query.get_or_404(note_id)
    html_text = md_to_html(note.content_md)
    return render_template("notes/show.html", note=note, html_text=html_text)


@app.route("/notes/<int:note_id>/edit")
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template("notes/edit.html", note=note)


@app.route("/notes/<int:note_id>/update", methods=["POST"])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)

    note.title = request.form["title"]
    note.content_md = request.form["content_md"]

    db.session.commit()

    flash("ノートを更新しました。", "info")

    return redirect(f"/notes/{note.id}")


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    db.session.delete(note)
    db.session.commit()

    flash("ノートを削除しました。", "danger")

    return redirect("/notes")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
