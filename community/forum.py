from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from pi_cryptoconnect.database import db
from pi_cryptoconnect.models import User, Post
from wtforms import Form, StringField, TextAreaField, validators

forum_blueprint = Blueprint('forum', __name__)

class PostForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    content = TextAreaField('Content', [validators.Length(min=1)])

@forum_blueprint.route('/forum', methods=['GET'])
def forum_index():
    """
    Display the forum index page with pagination.

    :return: Forum index page
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page, per_page=10)  # 10 posts per page
    return render_template('forum/index.html', posts=posts)

@forum_blueprint.route('/forum/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """
    Create a new forum post.

    :return: Redirect to forum index page
    """
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('forum.forum_index'))
    return render_template('forum/create.html', form=form)

@forum_blueprint.route('/forum/<int:post_id>', methods=['GET'])
def view_post(post_id):
    """
    View a forum post.

    :param post_id: Post ID
    :return: Post page
    """
    post = Post.query.get_or_404(post_id)
    return render_template('forum/post.html', post=post)

@forum_blueprint.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors.

    :param error: Error object
    :return: 404 error page
    """
    return render_template('404.html'), 404

@forum_blueprint.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors.

    :param error: Error object
    :return: 500 error page
    """
    db.session.rollback()  # Rollback the session on error
    return render_template('500.html'), 500
