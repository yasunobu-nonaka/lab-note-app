def test_login_required(client):
    res = client.get("/notes/1")
    assert res.status_code == 302
    assert "/login" in res.headers["location"]

def register(client):
    res = client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "password123",
        },
        follow_redirects=True,
    )

    return res

def login(client):
    res = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "password123",
        },
        follow_redirects=True,
    )

    return res

def create_note(client):
    res = client.post(
        "/notes",
        data={
            "title": "テストノート",
            "content_md": "- 要素１\n- 要素２\n- 要素３",
        },
        follow_redirects=True,
    )

    return res

def test_notes_index(client):
    register(client)
    login(client)
    res = client.get("/notes/")
    assert res.status_code == 200

def test_note_creation(client):
    register(client)
    res = login(client)
    assert res.status_code == 200

    res = create_note(client)
    assert res.status_code == 200
