from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, IPAddress, URL
from wtforms.validators import DataRequired
from app.models import User, Url
import requests
import threading
from socket import gaierror, gethostbyname
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlparse
from time import gmtime, strftime
from config import refresh_interval, filename, site_down

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class UrlForm(FlaskForm):
    urlname = StringField('Urlname', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_urlname(self, urlname):
        url = Url.query.filter_by(urlname=urlname.data).first()
        if url is not None:
            raise ValidationError('Please use a different url address.')

    def is_reachable(url):
        try:
            gethostbyname(url)
        except (gaierror):
            return False
        else:
            return True
    
    def get_status_code(url):
        try:
            status_code = requests.get(url, timeout=30).status_code
            return status_code
        except requests.ConnectionError:
            return site_down

    def check_single_url(url):
        if is_reachable(urlparse(url).hostname) == True:
            return str(get_status_code(url))
        else:
            return site_down