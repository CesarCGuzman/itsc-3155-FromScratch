from flask.testing import FlaskClient
from src.models.repositories import AppUserRepository
from app import app
from models import db, AppUser

def test_signin_page(test_app:FlaskClient):
    with app.app_context():
        # setup
        new_user = AppUser(username='john',
                            user_password= 12345678)
                            
        db.session.add(new_user)
        db.session.commit() 
        
        #run action
        res = test_app.get('/signin')
        page_data: str = res.data.decode

        #asserts
        assert res.status_code == 200
        assert f'<td><a href="/signin/{new_user.user_id}">john</a></td>' in page_data
        