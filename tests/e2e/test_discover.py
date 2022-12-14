from flask.testing import FlaskClient
from models import Scratch, AppUser, db

def test_discover_empty(test_app: FlaskClient):
    test_user = AppUser(username='Blue', user_password="password")
    db.session.add(test_user)
    db.session.commit()
    response = test_app.get('/discover')
    assert response.status_code == 302
    assert b'<div class="scratch-card ms-1 mt-1">' not in response.data

def test_discover(test_app: FlaskClient):
    new_scratch = Scratch(caption="hello", author_id=1)
    db.session.add(new_scratch)
    db.session.commit()

    response = test_app.get("/discover")
    assert response.status_code == 302
    assert b'<div class="scratch-card ms-1 mt-1">' in response.data
    assert b'hello' in response.data