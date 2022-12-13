from flask import session

def test_modify_session(client):
    with client.session_transaction() as session:
        session["user_id"] =1

        #session is saved now
    response = client.get("/users/me")
    assert response.json["username"] == "flask"
