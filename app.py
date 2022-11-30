import os
from flask import Flask, request, render_template, redirect, jsonify
from werkzeug.utils import secure_filename
from binascii import a2b_base64


UPLOAD_FOLDER = '/src/images'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# REPLACE WITH SESSION HANDLING :)
SIGNED_IN: bool = False 
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
        return redirect('discover.html')
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

@app.route('/compose-reply/scratch')
def compose_reply_scratch():
    return render_template('compose-reply-scratch.html')

@app.get('/Discover')
def discover():
    return render_template('discover.html')

@app.get('/notification')
def notification():
    return render_template('notification.html')

@app.get('/profile')
def profile():
    return render_template('profile.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.post("/imgProcessing")
def process_img():
    image_json = request.get_json()
    print(image_json)
    image_data = image_json.split(",")[1]
    binary_data = a2b_base64(image_data)

    # Replace with proper naming system
    with open('image.jpeg', 'wb') as file_writer:
        file_writer.write(binary_data)  
        print("wrote to image.jpeg!!")

    # image.filename = "userID_scratchID.jpeg" #This is currently incorrect - Just adding it because we will likely need it
    # safe_image = secure_filename(image.filename)
    # if image:
    #     image.save(os.path('static', 'images', safe_image))
    return redirect('/')