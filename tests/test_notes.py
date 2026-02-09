def test_login_required(client):
    res = client.get("/notes/1")
    assert res.status_code == 302
    assert "/login" in res.headers["location"]

def register(client):
    client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "password123",
        },
        follow_redirects=True,
    )


def login(client):
    client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "password123",
        },
        follow_redirects=True,
    )


def test_notes_index(client):
    register(client)
    login(client)
    res = client.get("/notes/")
    assert res.status_code == 200
