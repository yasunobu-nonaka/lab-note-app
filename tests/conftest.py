import pytest
from app import create_app
from app.models import db
from app.models import User, Note

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
def logged_in_client(client):
    client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "password123",
            "confirm": "password123",
        },
        follow_redirects=True,
    )
    
    client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "password123",
        },
        follow_redirects=True,
    )

    return client
