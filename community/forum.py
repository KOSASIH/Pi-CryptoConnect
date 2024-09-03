from flask import Blueprint, render_template, request, redirect, url_for
from pi_cryptoconnect.database import db
from pi_cryptoconnect.models import User, Post

forum_blueprint = Blueprint('forum', __name__)

@forum_blueprint.route('/forum', methods=['GET'])
def forum_index():
    """
    Display the forum index page.

    :return: Forum index page
    """
    posts = Post.query.all()
    return render_template('forum/index.html', posts=posts)

@forum_blueprint.route('/forum/create', methods=['GET', 'POST'])
def create_post():
    """
    Create a new forum post.

    :return: Redirect to forum index page
    """
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = request.user.id
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('forum.forum_index'))
    return render_template('forum/create.html')

@forum_blueprint.route('/forum/<int:post_id>', methods=['GET'])
def view_post(post_id):
    """
    View a forum post.

    :param post_id: Post ID
    :return: Post page
    """
    post = Post.query.get_or_404(post_id)
    return render_template('forum/post.html', post=post)
