from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required
from urllib.parse import urlparse

from ..models import db, User
from . import auth_bp

from ..forms.auth import RegistrationForm, LoginForm

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash("そのユーザー名はすでに使われています。", "danger")
            return redirect(url_for("auth.register"))

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("ユーザー登録が完了しました。", "success")

        return redirect(url_for("notes.notes_index")) # ノート一覧へ

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("ログインしました。", "success")

            next_page = request.form.get("next")
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("notes.notes_index")

            return redirect(next_page)
        else:
            flash("ユーザー名またはパスワードが違います。", "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "info")
    return redirect(url_for("auth.login"))
