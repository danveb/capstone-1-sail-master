from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField # username, password 
from wtforms.validators import InputRequired, Length # for required 

# RegisterForm 
class RegisterForm(FlaskForm):
    # fields 
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5)])
    email = StringField('Email', validators=[InputRequired(), Length(min=4, max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=20)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=20)]) 

# LoginForm 
class LoginForm(FlaskForm):
    # fields 
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])