from os import getenv
from flask import Flask, request, render_template, redirect
from models import db
from src.models.repositories import ScratchRepositorySingleton as srs, AppUserRepository as ars
from src.models.helpers import DebugHelper as debug  # REMOVE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# REPLACE WITH SESSION HANDLING :)
SIGNED_IN: bool = True
# Replace the follwing with a database later :)
PLACEHOLDER_USERNAMES = ['fadborecasts86', 'aabootllianzs77', 'dittensmumbass55', 'shetherwtunnings95', 'temorsefulrartarys76', 'tallasterbowards58', 'wnterviewiriters85', 'meetingmarrieds5', 'aalnutswssumptions72', 'bcoresoyscouts71', 'cailboxmartloads47', 'geinekenhloves20', 'irgeuntends73', 'rhizzwofls16', 'prrogantarofits40', 'qboveauizs67', 'cinkerouckoos32', 'iwindlersllegals65', 'naitersgormals38', 'onamusedublongatas46', 'tauceshemselves96', 'iiglinpnspects73', 'ertisteanhances68', 'belchbunts56',
                         'mindlykustys92', 'paskbills86', 'mistakemaps30', 'teavenlyhalus72', 'lreviouspeadings19', 'sanolactruggles30', 'dimbobarts23', 'sandshakehhortbreads45', 'oeetperates51', 'hssueiealths80', 'sibjecretives21', 'utuffsntrues24', 'mtatussatures42', 'wmportanceiittys61', 'ponvictioncigs51', 'mranshiptacabres8', 'tlockcheres38', 'drashytaggers74', 'uhereaswrethras12', 'vcourgeselcros49', 'complexcreams39', 'deporterrisputes18', 'nthleteaaives79', 'cocationlounters96', 'sntilutakings98', 'wailronderfuls94']
PLACEHOLDER_EMAIL_DOMAINS = ['gmail', 'yahoo', 'microsoft', 'aol']


@app.route('/')
def index():
    """ Redirects user to the home page if signed in or signin page if not
    signed in.
    """
    if SIGNED_IN:
        return redirect('/discover')
    else:
        return redirect('/signin')

@app.get('/signin')
def signin():
    return render_template('signin.html',
                            placeholder_usernames=PLACEHOLDER_USERNAMES)

@app.get('/signup')
def signup():
    return render_template('signup.html',
                            placeholder_usernames=PLACEHOLDER_USERNAMES,
                            placeholder_email_domains=PLACEHOLDER_EMAIL_DOMAINS)
@app.post('/signup')
def try_signing_up():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

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
    all_scratches = srs.get_all_scratches()

    return render_template('discover.html', all_scratches=all_scratches)

@app.get('/profile')
def profile():
    return render_template('profile.html')

@app.get('/test')
def get_test_page():
    print('\t\tentered test')
    return render_template('test-create-scratch.html')

@app.post('/compose/scratch/post')
def post_scratch():
    caption = request.form.get('caption', type=str)
    author_id = request.form.get('author_id', type=int)
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
    print(user)
    return redirect('/test', 200)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

