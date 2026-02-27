from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from sqlalchemy import func

from ..models import db, Note, Tag
from ..utils import md_to_html
from . import notes_bp

from ..forms.notes import NewNoteForm, EditNoteForm, SearchForm


@notes_bp.route("/", methods=["GET"])
@login_required
def notes_index():
    form = SearchForm(request.args)

    page = request.args.get("page", 1, type=int)  # ページ番号
    per_page = 5  # 1ページあたりの表示数

    # 基本クエリ（ユーザーIDによる検索）
    stmt = db.select(Note).where(Note.user_id == current_user.id)

    # 検索ワードがある場合 => 検索ワードを含むノートのみ取得
    if form.q.data:
        keyword = f"%{form.q.data.strip()}%"
        stmt = stmt.where(Note.title.ilike(keyword))

    # 総件数取得
    count_stmt = db.select(func.count()).select_from(stmt.subquery())
    total = db.session.scalar(count_stmt)

    # 現在のページに該当するノートを取得
    stmt = (
        stmt.order_by(Note.updated_at.desc())
        .limit(per_page)
        .offset((page - 1) * per_page)
    )

    notes = db.session.scalars(stmt).all()

    # 必要なページ数を計算
    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "notes/index.html",
        notes=notes,
        form=form,
        page=page,
        total_pages=total_pages,
    )


@notes_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_note():
    form = NewNoteForm()

    if form.validate_on_submit():
        note = Note(
            user_id=current_user.id,
            title=form.title.data,
            content_md=form.content_md.data,
        )

        for field in form.tags:
            tagname = (field.tagname.data or "").strip()  # 前後の空白を削除

            if not tagname:
                continue

            # タグが既に存在するかをチェック
            tag = db.session.scalar(
                db.select(Tag).filter_by(
                    user_id=current_user.id, tagname=tagname
                )
            )

            # 見つからない => まだ作られていないタグ => 新規追加
            if not tag:
                tag = Tag(user_id=current_user.id, tagname=tagname)

            note.tags.append(tag)

        db.session.add(note)
        db.session.commit()

        flash("ノートを作成しました。", "success")

        return redirect(url_for("notes.show_note", note_id=note.id))

    return render_template("notes/new.html", form=form)


@notes_bp.route("/<int:note_id>")
@login_required
def show_note(note_id):
    note = db.first_or_404(
        db.select(Note).filter_by(id=note_id, user_id=current_user.id)
    )
    html_text = md_to_html(note.content_md)
    return render_template("notes/show.html", note=note, html_text=html_text)


@notes_bp.route("/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = db.first_or_404(
        db.select(Note).filter_by(id=note_id, user_id=current_user.id)
    )
    form = EditNoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content_md = form.content_md.data

        # 中間テーブルのノートとタグのリレーションを一度削除
        note.tags.clear()

        for field in form.tags:
            tagname = (field.tagname.data or "").strip()  # 前後の空白を削除

            if not tagname:
                continue

            # タグが既に存在するかをチェック
            tag = db.session.scalar(
                db.select(Tag).filter_by(
                    user_id=current_user.id, tagname=tagname
                )
            )

            # 見つからない => まだ作られていないタグ => 新規追加
            if not tag:
                tag = Tag(user_id=current_user.id, tagname=tagname)

            # 中間テーブルにリレーションを再度追加
            note.tags.append(tag)

        db.session.commit()
        flash("ノートを更新しました。", "info")

        return redirect(url_for("notes.show_note", note_id=note.id))

    return render_template("notes/edit.html", note=note, form=form)


@notes_bp.route("/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = db.first_or_404(
        db.select(Note).filter_by(id=note_id, user_id=current_user.id)
    )
    db.session.delete(note)
    db.session.commit()

    flash("ノートを削除しました。", "danger")

    return redirect(url_for("notes.notes_index"))
