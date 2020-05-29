from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Regexp

from app.models.User import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('This field requires a valid email address')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('This field requires a valid email address')])
    username = StringField('Username', validators=[DataRequired(),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'User name must have only letters, numbers, dots or '
                                                          'underscores')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password',
                                                                         message='Passwords must match.')])
    submit = SubmitField('Submit')

    def validate_user(self, username):
        user = User.query.filter_by(user_name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please user a different email address.')

# class PostForm(FlaskForm):
#     text