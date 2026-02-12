from app.models import User

def register_user(client, username, password, confirm):
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

def test_register(client, app):
    res = register_user(client, "shakesan", "oishishake1234", "oishishake1234")
    assert res.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(username="shakesan").first()
        assert user is not None


def test_short_password_register_rejected(client, app):
    res = register_user(client, "shakesan", "shake1234", "shake1234")
    assert res.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(username="shakesan").first()
        assert user is None

def test_no_confirm_register_rejected(client, app):
    res = register_user(client, "shakesan", "shake1234", "")
    assert res.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(username="shakesan").first()
        assert user is None


def test_duplicate_username_register_rejected(client, app):
    test_register(client, app)

    res = register_user(client, "shakesan", "password1234", "password1234")
    assert res.status_code == 200

    with app.app_context():
        users = User.query.filter_by(username="shakesan").all()
        assert len(users) == 1


def test_login(client, app):
    register_user(client, "shakesan", "oishishake1234", "oishishake1234")

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

