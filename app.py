from flask import Flask, render_template, redirect

app = Flask(__name__)
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
        return redirect('/home')
    else:
        return redirect('/signin')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/compose/scratch')
def compose_scratch():
    return render_template('compose-scratch.html')


@app.get('/signin')
def signin():
    return render_template('signin.html',
                            placeholder_usernames=PLACEHOLDER_USERNAMES)

@app.get('/signup')
def signup():
    return render_template('signup.html',
                            placeholder_usernames=PLACEHOLDER_USERNAMES,
                            placeholder_email_domains=PLACEHOLDER_EMAIL_DOMAINS)
