from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from utils import md_to_html
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.secret_key = "dev-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

jst = timezone(timedelta(hours=9))
aware_jst_time = datetime.now(jst)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content_md = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=aware_jst_time)
    updated_at = db.Column(
        db.DateTime, default=aware_jst_time, onupdate=aware_jst_time
    )

@app.route("/")
def index():
    return render_template("index.html")


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

    flash("ノートを作成しました。", "success")

    return render_template("notes/created.html", note=note)


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
