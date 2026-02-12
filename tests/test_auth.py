from app.models import User

def test_register(client, app):
    res = client.post(
        "/register",
        data={
            "username": "lion",
            "password": "lion12345678",
            "confirm": "lion12345678",
        },
        follow_redirects=True,
    )

    assert res.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(username="lion").first()
        assert user is not None

def test_login(client):
    client.post(
        "/register",
        data={
            "username": "newshake",
            "password": "newshake1234",
        },
        follow_redirects=True,
    )

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
