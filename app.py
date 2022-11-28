import os
from flask import Flask, request, render_template, redirect, session, url_for
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from models import db
from src.models.repositories import ScratchRepositorySingleton as srs, AppUserRepository as ars

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.session_key = os.getenv('APP_SECRET_KEY')

load_dotenv()
db.init_app(app)
bcrypt = Bcrypt(app)

# Replace the follwing with a database later :)
PLACEHOLDER_USERNAMES = ['fadborecasts86', 'aabootllianzs77', 'dittensmumbass55', 'shetherwtunnings95', 'temorsefulrartarys76', 'tallasterbowards58', 'wnterviewiriters85', 'meetingmarrieds5', 'aalnutswssumptions72', 'bcoresoyscouts71', 'cailboxmartloads47', 'geinekenhloves20', 'irgeuntends73', 'rhizzwofls16', 'prrogantarofits40', 'qboveauizs67', 'cinkerouckoos32', 'iwindlersllegals65', 'naitersgormals38', 'onamusedublongatas46', 'tauceshemselves96', 'iiglinpnspects73', 'ertisteanhances68', 'belchbunts56',
                        'mindlykustys92', 'paskbills86', 'mistakemaps30', 'teavenlyhalus72', 'lreviouspeadings19', 'sanolactruggles30', 'dimbobarts23', 'sandshakehhortbreads45', 'oeetperates51', 'hssueiealths80', 'sibjecretives21', 'utuffsntrues24', 'mtatussatures42', 'wmportanceiittys61', 'ponvictioncigs51', 'mranshiptacabres8', 'tlockcheres38', 'drashytaggers74', 'uhereaswrethras12', 'vcourgeselcros49', 'complexcreams39', 'deporterrisputes18', 'nthleteaaives79', 'cocationlounters96', 'sntilutakings98', 'wailronderfuls94']
PLACEHOLDER_EMAIL_DOMAINS = ['gmail', 'yahoo', 'microsoft', 'aol']
 
@app.route('/')
def index():
    """ Redirects user to the home page if signed in or signin page if not
    signed in.
    """
    if 'user' in session:
        return redirect ('/discover.html')
    else:
        return redirect('/signin')

@app.get('/signin')
def signin_get():
    return redirect('/signin')

@app.post('/signin')
def signin_post():
    session['url'] = url_for('try_signing_in')
    
    username = request.form.get('username')
    password = request.form.get('password')

    existing_user = ars.return_user_by_username(username=username)
    if not existing_user:
        return redirect('/signin', user_not_exist=True)

    if not Bcrypt.check_password_hash(existing_user.password, password):
        return redirect('/signin', incorrect_password=True)

    session['user'] = {
        'user_id': existing_user.user_id
    }
    
    return render_template(url_for('discover'))      
                           
@app.get('/signup')
def signup_get():
    return redirect('/signup')

@app.post('/signup')
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    username_taken = ars.check_if_user_exists_by_username(username)
    if username_taken:
        return redirect('/signup', username_taken=True)

    if password != confirm_password:
        return redirect('/signup', passwords_match=False)

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

def hash_password(password: str) -> str:
    num_rounds = int(os.getenv('BCRYPT_ROUNDS'))
    hashed_bytes = bcrypt.generate_password_hash(password, num_rounds)
    hashed_password = hashed_bytes.decode('utf-8')

    return hashed_password

@app.get('/discover')
def discover_get():
    if 'user' not in session:
        return redirect('/')
    all_scratches = srs.get_all_scratches()
    return render_template('discover.html', all_scratches=all_scratches)


@app.get('/compose/scratch')
def compose_scratch_get():
   return render_template('compose-scratch.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.get('/user/<int:user_id>')
def user_get(user_id):
    redirect_to_signin_if_not_in_session()
    session_user_id = get_user_id_from_session()
    if session_user_id == user_id:
        is_user_owner = True
    else:
        is_user_owner = False

    user = ars.return_user_if_exists(user_id)
    all_scratches = ars.get_scratches_by_author(user_id)
    num_scratches = ars.get_total_number_of_scratches(user_id)
    num_likes = ars.get_total_number_of_likes_on_scratches(user_id)
    return render_template(
        'user.html',
        is_user_owner=is_user_owner,
        user=user,
        all_scratches=all_scratches,
        num_likes=num_likes,
        num_scratches=num_scratches
    )

@app.post('/user/<int:user_id>')
def user_post(user_id):
    # TODO: Implement bio updating later
    pass 


def get_user_id_from_session() -> int:
    if not user_in_session():
        raise ValueError('User is not in the session')

    return int(session['user']['user_id'])


def user_in_session() -> bool:
    return True if 'user' in session else False


@app.get('/test')
def get_test_page():
    print('\t\tentered test')
    return render_template('test-create-scratch.html')


@app.post('/compose/scratch/post')
def post_scratch():
    redirect_to_signin_if_not_in_session()
    
    author_id = get_user_id_from_session()
    caption = request.form.get('caption', type=str)
    is_comment = request.form.get('is_comment', type=bool)
    if is_comment is None or is_comment is False:
        is_comment = False
        scratch = srs.create_scratch(img=None,
                                    caption=caption,
                                    author_id=author_id,
                                    is_comment=False,
                                    return_scratch=True)
        print(scratch)
    else:
        op_scratch_id = request.form.get('op_scratch_id', type=int)
        scratch = srs.comment_on_scratch(img=None,
                                    caption=caption,
                                    op_scratch_id=op_scratch_id,
                                    author_id=author_id,
                                    return_scratch=True)
            

    return redirect(f'/scratch/{scratch.scratch_id}', 200)

def redirect_to_signin_if_not_in_session():
    if not user_in_session():
        return redirect('/signin')

@app.post('/like')
def like_scratch():
    redirect_to_signin_if_not_in_session()
    author_id = get_user_id_from_session()
    scratch_id = request.form.get('scratch_id', type=int)

    ars.like_scratch(author_id=author_id,
                     scratch_id=scratch_id)
    return redirect('/test', 200)  # FIXME: Replace with previous session url

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

