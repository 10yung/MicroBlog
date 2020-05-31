from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app.models.User import User

main = Blueprint('main', __name__)


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', message=e), 404



@main.route('/')
def index():
    return render_template('index.html')


@main.route('/post', methods=['GET'])
@login_required
def post():
    return render_template('post.html', name=current_user.user_name)


@main.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    user = User.query.filter_by(user_name=username).first_or_404()
    return render_template('profile.html', name=user)
