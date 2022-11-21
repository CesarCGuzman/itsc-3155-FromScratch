import os
from flask import Flask, request, render_template, redirect, session
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from models import db, User
<<<<<<< Updated upstream

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.session_key = os.getenv('APP_SECRET_KEY')

db.init_app(app)

bcyrpt = Bcrypt(app)

=======
 
load_dotenv()
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.session_key = os.getenv('APP_SECRET_KEY')
 
db.init_app(app)
 
bcyrpt = Bcrypt(app)
 
>>>>>>> Stashed changes
# REPLACE WITH SESSION HANDLING :)
SIGNED_IN: bool = False
# Replace the follwing with a database later :)
PLACEHOLDER_USERNAMES = ['fadborecasts86', 'aabootllianzs77', 'dittensmumbass55', 'shetherwtunnings95', 'temorsefulrartarys76', 'tallasterbowards58', 'wnterviewiriters85', 'meetingmarrieds5', 'aalnutswssumptions72', 'bcoresoyscouts71', 'cailboxmartloads47', 'geinekenhloves20', 'irgeuntends73', 'rhizzwofls16', 'prrogantarofits40', 'qboveauizs67', 'cinkerouckoos32', 'iwindlersllegals65', 'naitersgormals38', 'onamusedublongatas46', 'tauceshemselves96', 'iiglinpnspects73', 'ertisteanhances68', 'belchbunts56',
                        'mindlykustys92', 'paskbills86', 'mistakemaps30', 'teavenlyhalus72', 'lreviouspeadings19', 'sanolactruggles30', 'dimbobarts23', 'sandshakehhortbreads45', 'oeetperates51', 'hssueiealths80', 'sibjecretives21', 'utuffsntrues24', 'mtatussatures42', 'wmportanceiittys61', 'ponvictioncigs51', 'mranshiptacabres8', 'tlockcheres38', 'drashytaggers74', 'uhereaswrethras12', 'vcourgeselcros49', 'complexcreams39', 'deporterrisputes18', 'nthleteaaives79', 'cocationlounters96', 'sntilutakings98', 'wailronderfuls94']
PLACEHOLDER_EMAIL_DOMAINS = ['gmail', 'yahoo', 'microsoft', 'aol']
 
 
 
 
@app.route('/')
def index():
<<<<<<< Updated upstream
    """ Redirects user to the home page if signed in or signin page if not
    signed in.
    """
    if 'user' in session:
        return redirect ('/discover.html')
    #if SIGNED_IN:
        #return redirect('discover.html')
    #else:
        #return redirect('/signin')

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

=======
   """ Redirects user to the home page if signed in or signin page if not
   signed in.
   """
   if 'user' in session:
       return redirect ('/discover.html')
   #if SIGNED_IN:
       #return redirect('discover.html')
   #else:
       #return redirect('/signin')
 
      
 
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
 
>>>>>>> Stashed changes
@app.get('/signup')
def signup():
   return render_template('signup.html',
                           placeholder_usernames=PLACEHOLDER_USERNAMES,
                           placeholder_email_domains=PLACEHOLDER_EMAIL_DOMAINS)
@app.post('/signup')
def try_signing_up():
<<<<<<< Updated upstream
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    #SESSION IMPLEMENTATION
    existing_user = User.query.filter_by(username = username).first() #Makes sure there is only that one username in the query
    if existing_user:
        return redirect('/signin')
    
    hashed_bytes = Bcrypt.generate_password_hash (password, int(os.getenv('BCRYPT_ROUNDS'))) #hashes the passcode
    hashed_password = hashed_bytes.decode('utf-8')
    

    new_user = User(username,hashed_password) #creates a new user 

    db.session.add(new_user)
    db.session.commit()
    #END OF SESSION FOR THIS PART

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

    

=======
   username = request.form.get('username')
   password = request.form.get('password')
   confirm_password = request.form.get('confirm-password')
 
   #SESSION IMPLEMENTATION
   existing_user = User.query.filter_by(username = username).first() #Makes sure there is only that one username in the query
   if existing_user:
       return redirect('/signin')
  
   hashed_bytes = Bcrypt.generate_password_hash (password, int(os.getenv('BCRYPT_ROUNDS'))) #hashes the passcode
   hashed_password = hashed_bytes.decode('utf-8')
  
 
   new_user = User(username,hashed_password) #creates a new user
 
   db.session.add(new_user)
   db.session.commit()
   #END OF SESSION FOR THIS PART
 
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
 
  
 
>>>>>>> Stashed changes
@app.route('/compose/scratch')
def compose_scratch():
   return render_template('compose-scratch.html')
 
@app.get('/discover')
def discover():
<<<<<<< Updated upstream
    if 'user' not in session:
        return redirect('/')
    return render_template('discover.html')

=======
   if 'user' not in session:
       return redirect('/')
   return render_template('discover.html')
 
>>>>>>> Stashed changes
@app.get('/profile')
def profile():
   return render_template('profile.html')
 
@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html'), 404
