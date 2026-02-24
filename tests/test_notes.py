from app.models import db, User, Note


def request_note_creation(client, title, content_md):
    res = client.post(
        "/notes/new",
        data={
            "title": title,
            "content_md": content_md,
        },
        follow_redirects=True,
    )

    return res


#############################################
# tests for authorization
#############################################


def test_login_required(client):
    res = client.get("/notes/")
    assert res.status_code == 302
    assert "/login" in res.headers["location"]


def test_notes_index(logged_in_client):
    res = logged_in_client.get("/notes/", follow_redirects=True)
    assert res.status_code == 200
    assert "ノート一覧" in res.text
    assert "まだノートがありません。" in res.text


#############################################
# tests for note creation
#############################################


def test_note_creation(logged_in_client, app):
    res = request_note_creation(
        logged_in_client, "テストノート", "- 要素１\n- 要素２\n- 要素３"
    )
    assert len(res.history) == 1
    assert res.status_code == 200
    assert "ノートを作成しました。" in res.text
    assert "テストノート" in res.text

    with app.app_context():
        note = db.session.execute(
            db.select(Note).filter_by(title="テストノート")
        ).scalar_one_or_none()
        assert note is not None


def test_no_title_note_creation_rejected(logged_in_client):
    res = request_note_creation(
        logged_in_client, "", "- 要素１\n- 要素２\n- 要素３"
    )
    assert len(res.history) == 0
    assert res.status_code == 200
    assert "タイトルは必須です" in res.text
    assert "新規ノート作成" in res.text
    assert res.request.path == "/notes/new"


def test_too_long_title_note_creation_rejected(logged_in_client):
    res = request_note_creation(
        logged_in_client,
        "note_title" * 20 + "1",
        "- 要素１\n- 要素２\n- 要素３",
    )
    assert len(res.history) == 0
    assert res.status_code == 200
    assert "タイトルは200文字以内で入力してください" in res.text
    assert "新規ノート作成" in res.text
    assert res.request.path == "/notes/new"


def test_notes_index_shows_note(logged_in_client, app):
    with app.app_context():
        user = db.session.execute(db.select(User)).scalar_one_or_none()

        note = Note(
            user_id=user.id, title="テストノート", content_md="ノートの内容"
        )

        db.session.add(note)
        db.session.commit()

    res = logged_in_client.get("/notes/", follow_redirects=True)

    assert res.status_code == 200
    assert "テストノート" in res.text


#############################################
# test for note edit
#############################################
def test_note_edit(logged_in_client, app):
    with app.app_context():
        user = db.session.execute(db.select(User)).scalar_one_or_none()

        note = Note(
            user_id=user.id, title="テストノート", content_md="ノートの内容"
        )

        db.session.add(note)
        db.session.commit()

        note_id = note.id

    res = logged_in_client.post(
        f"/notes/{note_id}/edit",
        data={
            "title": "テストノート（日付）",
            "content_md": "おもしろいノートの内容",
        },
        follow_redirects=True,
    )
    assert len(res.history) == 1
    assert res.status_code == 200
    assert "ノートを更新しました。" in res.text
    assert "テストノート（日付）" in res.text

    with app.app_context():
        note = db.session.get(Note, note_id)
        assert note.title == "テストノート（日付）"
        assert note.content_md == "おもしろいノートの内容"


#############################################
# test for delete note
#############################################
def test_delete_note(logged_in_client, app):
    with app.app_context():
        user = db.session.execute(db.select(User)).scalar_one_or_none()

        note = Note(
            user_id=user.id, title="テストノート", content_md="ノートの内容"
        )

        db.session.add(note)
        db.session.commit()

        note_id = note.id

    res = logged_in_client.post(
        f"/notes/{note_id}/delete", follow_redirects=True
    )

    assert len(res.history) == 1
    assert res.status_code == 200
    assert "ノートを削除しました。" in res.text

    with app.app_context():
        note = db.session.get(Note, note_id)
        assert note is None


#############################################
# test for note authorization
#############################################


def test_notes_index_does_not_show_others_notes(logged_in_client, app):
    with app.app_context():
        user_a = db.session.execute(
            db.select(User).filter_by(username="testuser")
        ).scalar_one_or_none()

        user_b = User(username="testuser2")
        user_b.set_password("password21234")
        db.session.add(user_b)
        db.session.commit()

        note_a = Note(
            user_id=user_a.id,
            title="ユーザーA作成ノート",
            content_md="ユーザーAが作成したノート",
        )

        note_b = Note(
            user_id=user_b.id,
            title="ユーザーB作成ノート",
            content_md="ユーザーBが作成したノート",
        )
        db.session.add_all([note_a, note_b])
        db.session.commit()

    res = logged_in_client.get("/notes/")

    assert res.status_code == 200
    assert "ユーザーA作成ノート" in res.text
    assert "ユーザーB作成ノート" not in res.text


def test_cannot_accesss_others_note_detail(logged_in_client, app):
    with app.app_context():
        user_b = User(username="testuser2")
        user_b.set_password("password21234")
        db.session.add(user_b)
        db.session.commit()

        note_b = Note(
            user_id=user_b.id,
            title="ユーザーB作成ノート",
            content_md="ユーザーBが作成したノート",
        )
        db.session.add(note_b)
        db.session.commit()

        note_b_id = note_b.id

    res = logged_in_client.get(f"/notes/{note_b_id}")

    assert res.status_code == 404
    assert "Not Found" in res.text
    assert "ユーザーB作成ノート" not in res.text


#############################################
# test for note search
#############################################


def test_note_search(logged_in_client, app):
    with app.app_context():
        user = db.session.execute(db.select(User)).scalar_one_or_none()

        note_1 = Note(
            user_id=user.id,
            title="cooking",
            content_md="cooking is fun",
        )

        note_2 = Note(
            user_id=user.id,
            title="fishing",
            content_md="fishing is fun",
        )

        note_3 = Note(
            user_id=user.id,
            title="driving",
            content_md="driving is fun",
        )

        db.session.add_all([note_1, note_2, note_3])
        db.session.commit()

    res = logged_in_client.get("/notes/?q=fishing", follow_redirects=True)

    assert res.status_code == 200
    assert "fishing" in res.text
    assert "cooking" not in res.text
    assert "driving" not in res.text
