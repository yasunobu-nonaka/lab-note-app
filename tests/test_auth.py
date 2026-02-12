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
    res = register_user(client, "lion", "lion12345678", "lion12345678")
    assert res.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(username="lion").first()
        assert user is not None


def test_short_password_rejected(client, app):
    res = register_user(client, "lion", "lion1234", "lion1234")
    assert res.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(username="lion").first()
        assert user is None

def test_no_confirm_rejected(client, app):
    res = register_user(client, "lion", "lion1234", "")
    assert res.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(username="lion").first()
        assert user is None


def test_duplicate_username_rejected(client, app):
    test_register(client, app)

    res = register_user(client, "lion", "password1234", "password1234")
    assert res.status_code == 200

    with app.app_context():
        users = User.query.filter_by(username="lion").all()
        assert len(users) == 1


def test_login(client, app):
    register_user(client, "newshake", "newshake1234", "newshake1234")

    res = client.post(
        "/login",
        data={
            "username": "newshake",
            "password": "newshake1234",
        },
        follow_redirects=True,
    )

    assert len(res.history) == 1
    assert res.status_code == 200
