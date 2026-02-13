import pytest
from app import create_app
from app.models import db
from app.models import User, Note


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


@pytest.fixture
def app():
    app = create_app(config_name="testing")

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logged_in_client(client, app):
    create_user(app, "testuser", "password1234")

    client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "password1234",
        },
        follow_redirects=True,
    )

    return client
