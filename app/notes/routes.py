from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user

from ..models import db, Note
from ..utils import md_to_html
from . import notes_bp

from ..forms.notes import NewNoteForm, EditNoteForm


@notes_bp.route("/")
@login_required
def notes_index():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
    return render_template("notes/index.html", notes=notes)


@notes_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_note():
    form = NewNoteForm()

    if form.validate_on_submit():
        user_id = current_user.id
        title = form.title.data
        content_md = form.content_md.data

        note = Note(user_id=user_id, title=title, content_md=content_md)
        db.session.add(note)
        db.session.commit()

        html_text = md_to_html(note.content_md)

        flash("ノートを作成しました。", "success")

        return render_template("notes/created.html", note=note, html_text=html_text)

    return render_template("notes/new.html", form=form)

@notes_bp.route("/<int:note_id>")
@login_required
def show_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()
    html_text = md_to_html(note.content_md)
    return render_template("notes/show.html", note=note, html_text=html_text)


@notes_bp.route("/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    form = EditNoteForm(obj=note)

    if form.validate_on_submit():
        form.populate_obj(note) # フォームの値をモデルへ反映する
        
        db.session.commit()
        flash("ノートを更新しました。", "info")

        return redirect(url_for('notes.show_note', note_id=note.id))        

    return render_template("notes/edit.html", note=note, form=form)


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