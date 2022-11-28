import os
from flask import Flask, request, render_template, redirect, session
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from models import db
from src.models.repositories import ScratchRepositorySingleton as srs, AppUserRepository as ars

load_dotenv()
db.init_app(app)
bcyrpt = Bcrypt(app)
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.session_key = os.getenv('APP_SECRET_KEY')

bcyrpt = Bcrypt(app)
 

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
def signin():
    username = request.form.get('username')
    password = request.form.get('password')

    existing_user = User.query.filter_by(username = username).first() #Makes sure there is only that one username in the query
    if not existing_user:
        return redirect('/signin')

    if not Bcrypt.check_password_hash(existing_user.password,password):
        return redirect('/signin')

    session['user'] = {
        'user_id': existing_user.user_id
    }
    #change at the end
    return render_template('signin.html',
                           placeholder_usernames=PLACEHOLDER_USERNAMES)      
                           
                           
@app.get('/signin')
def signin():
   username = request.form.get('username')
   password = request.form.get('password')
 
   existing_user = User.query.filter_by(username = username).first() #Makes sure there is only that one username in the query
   if not existing_user:
       return redirect('/signin')
 
   if not Bcrypt.check_password_hash(existing_user.password,password):
       return redirect('/signin')
 
   session['user'] = {
       'user_id': existing_user.user_id
   }
   if 'user' in session:
       return redirect ('/discover.html')
   return render_template('signin.html',
                          placeholder_usernames=PLACEHOLDER_USERNAMES)
 
@app.post('/signup')
def try_signing_up():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    existing_user = User.query.filter_by(username = username).first() #Makes sure there is only that one username in the query
    if existing_user:
        return redirect('/signin')
    
    hashed_bytes = Bcrypt.generate_password_hash (password, int(os.getenv('BCRYPT_ROUNDS'))) #hashes the passcode
    hashed_password = hashed_bytes.decode('utf-8')
    

    new_user = User(username,hashed_password) #creates a new user 

    db.session.add(new_user)
    db.session.commit()

    print(f'\t\t{username=}\n' \
          f'\t\t{password=}\n' \
          f'\t\t{confirm_password=}\n')
    if password != confirm_password:
        return render_template('signup.html',
                                placeholder_usernames=PLACEHOLDER_USERNAMES,
                                placeholder_email_domains=PLACEHOLDER_EMAIL_DOMAINS,
                                passwords_match=False)

    
    # NOTE: TEMPORARY username/password displaying to demonstrate form works
    return f'<h1>Your username is: {username}<h1>' \
           f'<h1>Your password is: {password}<h1>'

@app.route('/compose/scratch')
def compose_scratch():
   return render_template('compose-scratch.html')
 
@app.get('/discover')
def discover():
    if 'user' not in session:
        return redirect('/')
    return render_template('discover.html')
 
@app.get('/profile')
def profile():
   return render_template('profile.html')
 
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    all_scratches = srs.get_all_scratches()

    return render_template('discover.html', all_scratches=all_scratches)

@app.get('/user/<int:user_id>')
def user(user_id):
    is_user_owner = False # FIXME: Implmenet session to determine if this user is the currently logged in user
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

@app.get('/test')
def get_test_page():
    print('\t\tentered test')
    return render_template('test-create-scratch.html')

@app.post('/compose/scratch/post')
def post_scratch():
    caption = request.form.get('caption', type=str)
    author_id = request.form.get('author_id', type=int)  # FIXME: Replace this with session user information
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
            

    # TODO validate user input
    debug.print_objs(['caption', 'author_id', 'is_comment'], caption, author_id, is_comment)


    return redirect('/test', 200)

@app.post('/signup/createuser')
def create_user():
    username = request.form.get('username', type=str)
    user_password = request.form.get('user_password', type=str)

    # TODO validate user input
    user = ars.create_user(username=username,
                           user_password=user_password,
                           return_user=True)
    return redirect(f'/user/{user.user_id}', 200)

@app.post('/like')
def like_scratch():
    scratch_id = request.form.get('scratch_id', type=int)
    author_id = request.form.get('author_id', type=int)  # FIXME: Replace this with session user information
    ars.like_scratch(author_id=author_id,
                     scratch_id=scratch_id)
    return redirect('/test', 200)  # FIXME: Replace with previous session url

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

