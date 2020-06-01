from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import login_required, current_user
from app import db
from app.models.User import User
from app.models.Post import Post
from app.microblog.forms import PostForm
from app.widgets.alerts import alerts

main = Blueprint('main', __name__)


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', message=e), 404


@main.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)


@main.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(user_name=username).first_or_404()

    form = PostForm()
    # on post submitted
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash(alerts['post_success'])
        return redirect(url_for('main.user', username=user.user_name))

    posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    return render_template('profile.html', user=user, form=form, posts=posts, profile_page=True)
