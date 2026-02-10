from app.models import db, User, Note

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

def test_notes_index_shows_note(logged_in_client, app):
    with app.app_context():
        user = User.query.first()

        note = Note(
            user_id=user.id,
            title="テストノート",
            content_md="ノートの内容"
        )

        db.session.add(note)
        db.session.commit()

    res = logged_in_client.get("/notes/")

    html = res.data.decode("utf-8")

    assert res.status_code == 200
    assert "テストノート" in html

def test_notes_index_does_not_show_others_notes(logged_in_client, app):
    with app.app_context():
        user_a = User.query.first()

        user_b = User(username="testuser2")
        user_b.set_password("password21234")
        db.session.add(user_b)
        db.session.commit()

        note_a = Note(
            user_id=user_a.id,
            title="ユーザーA作成ノート",
            content_md="ユーザーAが作成したノート"
        )

        note_b = Note(
            user_id=user_b.id,
            title="ユーザーB作成ノート",
            content_md="ユーザーBが作成したノート"
        )
        db.session.add_all([note_a, note_b])
        db.session.commit()

    res = logged_in_client.get("/notes/")
    html = res.data.decode("utf-8")

    assert res.status_code == 200
    assert "ユーザーA作成ノート" in html
    assert "ユーザーB作成ノート" not in html

