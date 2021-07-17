import os 
import requests 

from flask import Flask, render_template, redirect, flash, session, g # Flask Global 
from flask_debugtoolbar import DebugToolbarExtension 
from sqlalchemy.exc import IntegrityError 
from forms import RegisterForm, LoginForm, VoyageForm 
from models import db, connect_db, User, Club, Voyage 

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
# User register/login/logout

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
def home_page():
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
            return render_template('user/register.html', form=form)

        do_login(user) 
        return redirect('/') 

    # GET Register Form 
    return render_template('user/register.html', form=form)

# GET & POST /login
@app.route('/login', methods=["GET", "POST"]) 
def login_user():
    # if "user_id" in session: 
    #     return redirect(f"/users/{session['user_id']}")
    # LoginForm instance 
    form = LoginForm() 
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data 
        # call authenticate (classmethod)
        user = User.authenticate(username, password) 
        if user:
            do_login(user)
            flash(f'Welcome back, {user.username}', 'success')
            return redirect(f'users/{user.id}')
        flash('Invalid credentials', 'danger')
        return redirect('/login') 

    # GET Login Form
    return render_template('user/login.html', form=form) 

# GET /logout 
@app.route('/logout')
def logout_user():
    do_logout() 
    flash('Successfully Logged Out', 'info')
    return redirect('/') 

##############################################################################
# User details 

# GET /userdetail
@app.route('/users/<int:user_id>') 
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user/user.html', user=user)

##############################################################################
# VoyageForm 

# GET & POST /voyage 
@app.route('/voyage', methods=["GET", "POST"]) 
def voyage(): 
    if not g.user: 
        flash('You do not have access', 'danger')
        return redirect('/')
    """Display Voyage Form"""
    clubs_choices = [(club.id, club.name) for club in Club.query.order_by('name').all()]
    form = VoyageForm() 
    form.start_point.choices = clubs_choices 
    form.end_point.choices = clubs_choices
    # form.end_point.choices = clubs_choices 
    if form.validate_on_submit():
        start_point = form.start_point.data 
        end_point = form.end_point.data
        new_voyage = Voyage(start_point=start_point, end_point=end_point)
        # db.session.add(new_voyage)
        g.user.voyage.append(new_voyage)
        db.session.commit() 
        flash('Voyage Created!', 'success')
        # return render_template('result.html')
        return redirect('/voyage')

    # Show voyages 
    voyages = (Voyage
                .query
                .order_by(Voyage.id)
                .all())
    return render_template('voyage/voyage.html', form=form, voyages=voyages) 

# GET 
@app.route('/voyage/<int:voyage_id>') 
def view_voyage(voyage_id):
    voyage = Voyage.query.get_or_404(voyage_id)
    return render_template('voyage/view.html', voyage=voyage)

##############################################################################
# Club details 

# GET /clubs
@app.route('/clubs')
def all_clubs():
    """Display Clubs"""
    clubs = Club.query.order_by(Club.name).all() 
    return render_template('club/clubs.html', clubs=clubs)

@app.route('/clubs/<int:club_id>')
def each_club(club_id):
    """Display Each Club"""
    club = Club.query.get_or_404(club_id)
    return render_template('club/details.html', club=club)