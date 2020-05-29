from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from app import db
from app.models.User import User
from app.widgets.alerts import alerts
from app.auth.forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # check if current user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # Initialize form
    form = LoginForm()

    # Action after received form data
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # If user record exist and password is correct
        # TODO: secure query string malicious injection, redirect to main page if un-wanted url is submitted
        if user is None or not user.check_password(form.password.data):
            flash(alerts['login_error'])
            return redirect(url_for('auth.login'))

        # If login success!
        login_user(user, form.remember_me.data)

        return redirect(url_for('main.index'))

    return render_template('auth/login.html', form=form, title='Sign In')


@auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # check if current user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    # Action after received form data
    if form.validate_on_submit():
        user = User(user_name=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Login automatically
        login_user(user)
        flash(alerts['login_success'])
        return redirect(url_for('main.index'))

    return render_template('auth/register.html', form=form, title='Register')