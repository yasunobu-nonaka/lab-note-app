from app.models import db, User
from conftest import request_register, create_user, request_login

#############################################
# tests for register
#############################################


def test_register(client, app):
    res = request_register(
        client, "shakesan", "oishishake1234", "oishishake1234"
    )
    assert res.status_code == 200

    with app.app_context():
        user = db.session.execute(
            db.select(User).filter_by(username="shakesan")
        ).scalar_one_or_none()
        assert user is not None


def test_short_password_register_rejected(client, app):
    res = request_register(client, "shakesan", "shake1234", "shake1234")
    assert res.status_code == 200

    with app.app_context():
        user = db.session.execute(
            db.select(User).filter_by(username="shakesan")
        ).scalar_one_or_none()
        assert user is None


def test_no_confirm_register_rejected(client, app):
    res = request_register(client, "shakesan", "shake1234", "")
    assert res.status_code == 200

    with app.app_context():
        user = db.session.execute(
            db.select(User).filter_by(username="shakesan")
        ).scalar_one_or_none()
        assert user is None


def test_duplicate_username_register_rejected(client, app):
    test_register(client, app)

    res = request_register(client, "shakesan", "password1234", "password1234")
    assert res.status_code == 200

    with app.app_context():
        stmt = db.select(User).filter_by(username="shakesan")
        users = db.session.execute(stmt).scalars().all()
        assert len(users) == 1


#############################################
# tests for login
#############################################


def test_login(client, app):
    create_user(app, "shakesan", "oishishake1234")

    res = request_login(client, "shakesan", "oishishake1234")

    assert len(res.history) == 1
    assert res.status_code == 200
    assert "ログインしました。" in res.text
    assert res.request.path == "/notes/"

    with client.session_transaction() as session:
        assert "_user_id" in session


def test_wrong_password_login_rejected(client, app):
    create_user(app, "shakesan", "oishishake1234")

    res = request_login(client, "shakesan", "moishishake1234")

    assert len(res.history) == 0
    assert res.status_code == 200
    assert "ユーザー名またはパスワードが違います。" in res.text

    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_no_password_login_rejected(client, app):
    create_user(app, "shakesan", "oishishake1234")

    res = request_login(client, "shakesan", "")

    assert len(res.history) == 0
    assert res.status_code == 200
    assert "パスワードは必須です" in res.text

    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_logout(client, app):
    create_user(app, "shakesan", "oishishake1234")

    request_login(client, "shakesan", "oishishake1234")

    res = client.get("/logout", follow_redirects=True)

    assert len(res.history) == 1
    assert res.status_code == 200
    assert "ログアウトしました。" in res.text
    assert res.request.path == "/login"

    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_logout_requires_login(client):
    res = client.get("/logout", follow_redirects=True)

    # redirectが1回発生
    assert len(res.history) == 1

    # loginページが表示される
    assert "ログイン" in res.text
