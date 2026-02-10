def test_register(client):
    res = client.post(
        "/register",
        data={
            "username": "lion",
            "password": "lion123",
        },
        follow_redirects=True,
    )

    assert res.status_code == 200

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
