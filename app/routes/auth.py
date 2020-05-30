from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from app import db
from app.models.User import User
from app.widgets.alerts import alerts
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from app.email import send_email

auth = Blueprint('auth', __name__)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


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
    flash(alerts['logout_success'])
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

        token = user.generate_token('confirm')
        send_email(user.email, 'Confirm Your Account',
                   'mail/confirm', user=user, token=token)

        # Login automatically
        login_user(user)
        flash(alerts['login_success'])
        return redirect(url_for('main.index'))

    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash(alerts['user_confirm_success'])
    else:
        flash(alerts['user_confirm_error'])
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_token('confirm')
    print(current_user)
    send_email(current_user.email, 'Confirm Your Account',
               'mail/confirm', user=current_user, token=token)
    flash(alerts['resent_confirm_email'])
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # If user is already login
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordRequestForm()

    # Action after received form data
    if form.validate_on_submit():
        # check if use is existed
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None:
            token = user.generate_token('reset')
            send_email(user.email, 'Reset Your Password',
               'mail/reset_password', user=user, token=token)
            flash(alerts['reset_password_request_sent'])
            return redirect(url_for('auth.login'))
        else:
            flash(alerts['reset_password_request_error'])
    return render_template('auth/reset_password_request.html', form=form, title='Reset password request')


@auth.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # if get user
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(alerts['reset_password_success'])
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)