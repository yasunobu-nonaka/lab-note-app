from app.models import db, User

def request_register(client, username, password, confirm):
    res = client.post(
        "/register",
        data={
            "username": username,
            "password": password,
            "confirm": confirm,
        },
        follow_redirects=True,
    )
    
    return res

def create_user(app, username, password):
    with app.app_context():
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

def request_login(client, username, password):
    res = client.post(
        "/login",
        data={
            "username": username,
            "password": password,
        },
        follow_redirects=True,
    )

    return res


#############################################
    # tests for register
#############################################

def test_register(client, app):
    res = request_register(client, "shakesan", "oishishake1234", "oishishake1234")
    assert res.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(username="shakesan").first()
        assert user is not None


def test_short_password_register_rejected(client, app):
    res = request_register(client, "shakesan", "shake1234", "shake1234")
    assert res.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(username="shakesan").first()
        assert user is None

def test_no_confirm_register_rejected(client, app):
    res = request_register(client, "shakesan", "shake1234", "")
    assert res.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(username="shakesan").first()
        assert user is None


def test_duplicate_username_register_rejected(client, app):
    test_register(client, app)

    res = request_register(client, "shakesan", "password1234", "password1234")
    assert res.status_code == 200

    with app.app_context():
        users = User.query.filter_by(username="shakesan").all()
        assert len(users) == 1

#############################################
    # tests for login
#############################################

def test_login(client, app):
    create_user(app, "shakesan", "oishishake1234")

    res = client.post(
        "/login",
        data={
            "username": "shakesan",
            "password": "oishishake1234",
        },
        follow_redirects=True,
    )

    assert len(res.history) == 1
    assert res.status_code == 200

    with client.session_transaction() as session:
        assert "_user_id" in session


def test_wrong_password_login_rejected(client, app):
    create_user(app, "shakesan", "oishishake1234")

    res = client.post(
        "/login",
        data={
            "username": "shakesan",
            "password": "moishishake1234",
        },
            follow_redirects=True,
    )

    assert len(res.history) == 0
    assert res.status_code == 200
    assert "ユーザー名またはパスワードが違います。" in res.text

    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_no_password_login_rejected(client, app):
    create_user(app, "shakesan", "oishishake1234")

    res = client.post(
        "/login",
        data={
            "username": "shakesan",
            "password": "",
        },
            follow_redirects=True,
    )

    assert len(res.history) == 0
    assert res.status_code == 200
    assert "パスワードは必須です" in res.text

    with client.session_transaction() as session:
        assert "_user_id" not in session
