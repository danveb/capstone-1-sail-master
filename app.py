import os 
import requests 

from flask import Flask, render_template, redirect, flash, session, g # Flask Global 
from flask_debugtoolbar import DebugToolbarExtension 
from sqlalchemy.exc import IntegrityError 
from forms import RegisterForm, LoginForm 
from models import db, connect_db, User, Club

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sail_master'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True 
app.config['SECRET_KEY'] = 'ashdjlfkeu9p13ejlkas'

connect_db(app)
db.create_all() 
debug = DebugToolbarExtension(app) 

CURRENT_USER = 'current_user' 

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If logged in, add current user to Flask global."""

    if CURRENT_USER in session:
        g.user = User.query.get(session[CURRENT_USER])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURRENT_USER] = user.id

def do_logout():
    """Logout user."""

    if CURRENT_USER in session:
        del session[CURRENT_USER]

@app.route('/')
def home():
    return render_template('index.html')

# GET/POST /register
@app.route('/register', methods=["GET", "POST"])
def register_user():
    # RegisterForm instance
    form = RegisterForm() 
    # form data back 
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data 
        # error handling? 
        user = User.register(username, password, email, first_name, last_name)

        # db
        db.session.add(user) 
        try:
            db.session.commit()
        except IntegrityError:
            flash('Username already taken', 'danger')
            return render_template('register.html', form=form)

        do_login(user) 
        return redirect('/') 

    # GET Register Form 
    return render_template('register.html', form=form)

# GET & POST /login
@app.route('/login', methods=["GET", "POST"]) 
def login_user():
    if "user_id" in session: 
        return redirect(f"/users/{session['user_id']}")
    # LoginForm instance 
    form = LoginForm() 
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data 
        # call authenticate (classmethod)
        user = User.authenticate(username, password) 
        if user:
            do_login(user) 
            flash(f'Welcome back, {user.username}')
            return redirect(f'/users/{user.username}')

        flash('Invalid credentials', 'danger')

    # GET Login Form
    return render_template('login.html', form=form) 

# GET /logout 
@app.route('/logout')
def logout_user():
    session.pop(CURRENT_USER) 
    flash('Successfully logged out', 'info')
    return redirect('/login') 