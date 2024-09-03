from flask import Blueprint, render_template, request, redirect, url_for
from pi_cryptoconnect.database import db
from pi_cryptoconnect.models import User, Strategy

marketplace_blueprint = Blueprint('marketplace', __name__)

@marketplace_blueprint.route('/marketplace', methods=['GET'])
def marketplace_index():
    """
    Display the marketplace index page.

    :return: Marketplace index page
    """
    strategies = Strategy.query.all()
    return render_template('marketplace/index.html', strategies=strategies)

@marketplace_blueprint.route('/marketplace/create', methods=['GET', 'POST'])
def create_strategy():
    """
    Create a new trading strategy.

    :return: Redirect to marketplace index page
    """
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        code = request.form['code']
        user_id = request.user.id
        strategy = Strategy(name=name, description=description, code=code, user_id=user_id)
        db.session.add(strategy)
        db.session.commit()
        return redirect(url_for('marketplace.marketplace_index'))
    return render_template('marketplace/create.html')

@marketplace_blueprint.route('/marketplace/<int:strategy_id>', methods=['GET'])
def view_strategy(strategy_id):
    """
    View a trading strategy.

    :param strategy_id: Strategy ID
    :return: Strategy page
    """
    strategy = Strategy.query.get_or_404(strategy_id)
    return render_template('marketplace/strategy.html', strategy=strategy)
