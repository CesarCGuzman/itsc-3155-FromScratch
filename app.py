import os
from flask import json
from binascii import a2b_base64
from flask import Flask, request, render_template, redirect, session, url_for
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from models import AppUser, db
from src.models.repositories import ScratchRepositorySingleton as srs, AppUserRepository as ars
from functools import wraps

UPLOAD_FOLDER = '/src/images'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.getenv('APP_SECRET_KEY')

load_dotenv()
db.init_app(app)
bcrypt = Bcrypt(app)
num_rounds = int(os.getenv('BCRYPT_ROUNDS'))

""" A decorator that determines what resources must have user auth
    to access. If user is not auth'd, they are redirected to sign in.
"""
def authenticated_resource(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)

        return redirect(url_for('signin_get'))

    return decorated_function


@app.route('/')
def index():
    """ Redirects user to the home page if signed in or signin page if not
    signed in.
    """
    session['url'] = url_for('index')
    if 'user' in session:
        return redirect(url_for('discover_get'))
    else:
        return redirect(url_for('signin_get'))


@app.get('/signin')
def signin_get(**kwargs):
    session['url'] = url_for('signin_get')
    return render_template('signin.html', **kwargs)


@app.post('/signin')
def signin_post():
    session['url'] = url_for('signin_post')

    username = request.form.get('username')
    password = request.form.get('password')

    user_exists = ars.check_if_user_exists_by_username(username=username)
    if not user_exists:
        return signin_get(user_exists=False, failed_username=username)

    existing_user = ars.return_user_by_username(username=username)
    if not bcrypt.check_password_hash(existing_user.user_password, password):
        return signin_get(incorrect_password=True)

    session['user'] = {
        'user_id': existing_user.user_id
    }

    return redirect(url_for('discover_get'))


@app.get('/signup')
def signup_get():
    session['url'] = url_for('signup_get')
    return render_template('signup.html')


@app.post('/signup')
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    response = request.get_json()

    validate_username(username)
    validate_password(password)

    username_taken = ars.check_if_user_exists_by_username(username)
    if username_taken:
        return redirect(url_for('signup_get', username_taken=True))

    if password != confirm_password:
        return redirect(url_for('signup_get', passwords_match=False))

    hashed_password = hash_password(password)

    user = ars.create_user(username=username,
                           user_password=hashed_password,
                           return_user=True)

    db.session.add(user)
    db.session.commit()

    session['user'] = {
        'user_id': user.user_id
    }

    return redirect(f'/user/{user.user_id}', 200)

def save_pfp_to_server(response, user):
    image_data = response.get('image_uri').split(',')[1]
    binary_data = a2b_base64(image_data)
    
    scratch_img_folder = 'static/scratches/'
    filename = user.pfp_filename

    with open(scratch_img_folder + filename, 'wb') as file_writer:
        file_writer.write(binary_data)  
        print(f"wrote to {filename}!!")


def validate_username(username):
    if len(username) < AppUser.MINIMUM_FRONTEND_USERNAME_LENGTH:
            raise ValueError(f'Username must be greater than ' + 
                             f'{AppUser.MINIMUM_FRONTEND_USERNAME_LENGTH} characters long')
    if len(username) > AppUser.MAXIMUM_FRONTEND_USERNAME_LENGTH:
        raise ValueError(f'Username must be less than ' + 
                            f'{AppUser.MAXIMUM_FRONTEND_USERNAME_LENGTH} characters long')

def validate_password(user_password):
    if len(user_password) < AppUser.MINIMUM_FRONTEND_PASSWORD_LENGTH:
            raise ValueError(f'Password must be greater than ' +  
                             f'{AppUser.MINIMUM_FRONTEND_PASSWORD_LENGTH} characters long')
    if len(user_password) > AppUser.MAXIMUM_FRONTEND_PASSWORD_LENGTH:
        raise ValueError(f'Password cannot be greater than ' +  
                            f'{AppUser.MAXIMUM_FRONTEND_PASSWORD_LENGTH} characters long')                    


def hash_password(password: str) -> str:
    hashed_bytes = bcrypt.generate_password_hash(password, num_rounds)
    hashed_password = hashed_bytes.decode('utf-8')

    return hashed_password


@app.get('/discover')
@authenticated_resource
def discover_get():
    session['url'] = url_for('discover_get')
    all_scratches = srs.get_all_scratches()
    return render_template('discover.html', all_scratches=all_scratches)


@app.get('/compose/scratch')
@authenticated_resource
def compose_scratch_get():
    session['url'] = url_for('compose_scratch_get')
    return render_template('compose-scratch.html')



@app.route('/compose-reply/scratch')
def compose_reply_scratch():
    return render_template('compose-reply-scratch.html')

  
@app.get('/discover')
def discover():
    if 'user' not in session:
        return redirect('/')
    return render_template('discover.html')

@app.get('/notification')
def notification():
    return render_template('notification.html')

 
@app.errorhandler(404)
def page_not_found(error):
    session['url'] = url_for('page_not_found')
    return render_template('404.html'), 404


@app.get('/user/<int:user_id>')
@authenticated_resource
def user_get(user_id):
    """ Returns a template for a particular user of `user_id`.

    Args:
        user_id (int): The user id of the user being accessed
"""
    session['url'] = url_for('user_get', user_id=user_id)
    user_page_template = load_user_page_from_id(user_id)
        
    return user_page_template


@app.get('/user')
@authenticated_resource
def profile():
    """ Returns a template for the currently signed-in user's profile view.
        The user is able to edit their biography in this page.
    """
    session['url'] = url_for('profile')
    session_user_id = get_user_id_from_session()
    user_page_template = load_user_page_from_id(session_user_id, is_owner=True)
    
    return user_page_template


def load_user_page_from_id(user_id: int, *, is_owner: bool = False) -> str:
    user = ars.return_user_by_id(user_id)
    all_scratches = ars.get_scratches_by_author(user_id)
    num_scratches = ars.get_total_number_of_scratches(user_id)
    num_likes = ars.get_total_number_of_likes_on_scratches(user_id)

    return render_template(
        'user.html',
        is_user_owner=is_owner,
        user=user,
        all_scratches=all_scratches,
        num_likes=num_likes,
        num_scratches=num_scratches
    )

@app.post('/user/<int:user_id>')
@authenticated_resource
def user_post(user_id):
    session['url'] = url_for('user_post')
    # TODO: Implement bio updating later
    pass


def get_user_id_from_session() -> int:
    if not user_is_in_session():
        raise ValueError('User is not in the session')

    return int(session['user']['user_id'])


def user_is_in_session() -> bool:
    return True if 'user' in session else False


@app.get('/test')
def get_test_page():
    print('\t\tentered test')
    return render_template('test-create-scratch.html')


@app.post('/compose/scratch/post')
@authenticated_resource
def post_scratch():
    session['url'] = url_for('post_scratch')
    # caption = request.form.get('caption')
    response = request.get_json()
    caption = response.get('caption') 
    session_author_id = get_user_id_from_session()

    scratch = srs.create_scratch(caption=caption,
                                 author_id=session_author_id,
                                 is_comment=False,
                                 return_scratch=True)
    save_scratch_to_server(response, scratch)
    
    return redirect(f'/scratch/{scratch.scratch_id}', 200)

def save_scratch_to_server(response, scratch):
    image_data = response.get('image_uri').split(',')[1]
    binary_data = a2b_base64(image_data)
    
    scratch_img_folder = 'static/scratches/'
    filename = scratch.scratch_filename

    with open(scratch_img_folder + filename, 'wb') as file_writer:
        file_writer.write(binary_data)  
        print(f"wrote to {filename}!!")


@app.post('/like')
@authenticated_resource
def like_scratch():
    author_id = get_user_id_from_session()
    scratch_id = request.form.get('scratch_id', type=int)

    ars.like_scratch(author_id=author_id,
                     scratch_id=scratch_id)
    previous_url = session.get('url')
    return redirect(previous_url)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404



@app.post('/logout')
def logout():
    session.pop('user')
    return redirect('/signin')



