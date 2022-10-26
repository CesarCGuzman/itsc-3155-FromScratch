from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compose/scratch')
def compose_scratch():
    return render_template('compose-scratch.html')