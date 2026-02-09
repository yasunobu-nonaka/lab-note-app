from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user

from ..models import db, Note
from ..utils import md_to_html
from . import notes_bp


@notes_bp.route("/")
@login_required
def notes_index():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
    return render_template("notes/index.html", notes=notes)


@notes_bp.route("/new")
@login_required
def new_note():
    return render_template("notes/new.html")


@notes_bp.route("/", methods=["POST"])
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


@notes_bp.route("/<int:note_id>")
@login_required
def show_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()
    html_text = md_to_html(note.content_md)
    return render_template("notes/show.html", note=note, html_text=html_text)


@notes_bp.route("/<int:note_id>/edit")
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()
    return render_template("notes/edit.html", note=note)


@notes_bp.route("/<int:note_id>/update", methods=["POST"])
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

    return redirect(url_for('notes.show_note', note_id=note.id))


@notes_bp.route("/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(note)
    db.session.commit()

    flash("ノートを削除しました。", "danger")

    return redirect(url_for('notes.notes_index'))