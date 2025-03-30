from flask import Blueprint, render_template, request
from pi_cryptoconnect.database import db
from pi_cryptoconnect.models import User, Strategy

leaderboard_blueprint = Blueprint('leaderboard', __name__)

@leaderboard_blueprint.route('/leaderboard', methods=['GET'])
def leaderboard_index():
    """
    Display the leaderboard page with sorting and pagination.

    :return: Leaderboard page
    """
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'profit', type=str)  # Default sorting by profit
    order = request.args.get('order', 'desc', type=str)  # Default order is descending

    # Fetch strategies and users from the database
    strategies = Strategy.query.all()
    users = User.query.all()

    # Sort strategies based on the selected criteria
    if sort_by == 'profit':
        strategies.sort(key=lambda x: x.profit, reverse=(order == 'desc'))
    elif sort_by == 'win_rate':
        strategies.sort(key=lambda x: x.win_rate, reverse=(order == 'desc'))
    # Add more sorting criteria as needed

    # Pagination logic
    per_page = 10
    total_strategies = len(strategies)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_strategies = strategies[start:end]

    return render_template('leaderboard/index.html', strategies=paginated_strategies, users=users, total_strategies=total_strategies, page=page, per_page=per_page)

@leaderboard_blueprint.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors.

    :param error: Error object
    :return: 404 error page
    """
    return render_template('404.html'), 404

@leaderboard_blueprint.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors.

    :param error: Error object
    :return: 500 error page
    """
    db.session.rollback()  # Rollback the session on error
    return render_template('500.html'), 500
