from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
from app.models import User

class LoginForm(FlaskForm): # Defining the types of data for each variable on login form
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm): # Defining the types of data for each variable on registration form
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),
        EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username): # Checks if username has already been used
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email): # Checks if email has already been used
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class RefillForm(FlaskForm): # Defining the type of data for each variable on refill form
    refill_val = IntegerField('Enter amount of water refilled in ml:', validators=[NumberRange(min=0, max=1000)])
    submit = SubmitField('Fill Bottle')
