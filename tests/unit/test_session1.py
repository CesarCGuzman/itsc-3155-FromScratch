from flask import session
def test_access_session(client):
    with client:
        client.post("/login", data={"username": "flask"})
        assert session["user_id"] == 1