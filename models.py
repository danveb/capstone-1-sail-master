from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect database sail_master"""
    db.app = app
    db.init_app(app) 

class User(db.Model):
    """User"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False) 
    # Relationship 
    # club = db.relationship('Club', backref='user', cascade='all, delete') 
    # voyage = db.relationship('Voyage', backref='user', cascade='all, delete') 

    # classmethod (register) -> Flask-Bcrypt
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user with hashed password & return user"""
        # turn password into a hash with bcrypt (returns a bytestring)
        hash_pw = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string to store in database
        hash_utf8 = hash_pw.decode('utf8')
        # return instance of user with username and hashed pwd 
        return cls(username=username, password=hash_utf8, email=email, first_name=first_name, last_name=last_name) 

    # classmethod (authenticate) -> Flask-Bcrypt 
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & pwd is correct
        Return user if valid; else return False 
        """
        user = User.query.filter_by(username=username).first() 
        if user and bcrypt.check_password_hash(user.password, pwd):
            # return user instance 
            return user
        else: 
            return False 

class Voyage(db.Model):
    """Voyage"""
    __tablename__ = 'voyages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # club_name = db.Column(db.Integer, db.ForeignKey('clubs.name'))


class Club(db.Model):
    """Club"""
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    lat = db.Column(db.Numeric, nullable=True)
    lon = db.Column(db.Numeric, nullable=True)
    tel = db.Column(db.Text, nullable=True) 
    url = db.Column(db.Text, nullable=True)
    # user = db.relationship('User', backref='club', cascade='all, delete')
    # voyage = db.relationship('Voyage', backref='club', cascade='all, delete')

