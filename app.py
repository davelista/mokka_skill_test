from flask import Flask, render_template
from flask import request
from forms import LoginForm
from flask_wtf import FlaskForm
import sqlite3 as sql
app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
@app.route('/')
def index():
    return 'Hello World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'hello world'
    else:
        form = LoginForm()
        return render_template('login.html', form=form)
