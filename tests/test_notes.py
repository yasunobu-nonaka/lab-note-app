def test_login_required(client):
    res = client.get("/notes/1")
    assert res.status_code == 302
    assert "/login" in res.headers["location"]

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

def test_notes_index(logged_in_client):
    res = logged_in_client.get("/notes/")
    assert res.status_code == 200

def test_note_creation(logged_in_client):
    res = create_note(logged_in_client)
    assert res.status_code == 200
