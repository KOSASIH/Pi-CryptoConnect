from flask import Blueprint, render_template
from pi_cryptoconnect.database import db
from pi_cryptoconnect.models import User, Strategy

leaderboard_blueprint = Blueprint('leaderboard', __name__)

@leaderboard_blueprint.route('/leaderboard', methods=['GET'])
def leaderboard_index():
    """
    Display the leaderboard page.

    :return: Leaderboard page
    """
    strategies = Strategy.query.all()
    users = User.query.all()
    return render_template('leaderboard/index.html', strategies=strategies, users=users)
