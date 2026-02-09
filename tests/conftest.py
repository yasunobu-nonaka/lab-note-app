import pytest
from app import create_app
from app.models import db
from app.models import User, Note

@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTFS_CSRF_ENABLED=False,
        LOGIN_DISABLED=False,
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
