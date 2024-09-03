from flask import Blueprint, render_template, request, redirect, url_for
from pi_cryptoconnect.database import db
from pi_cryptoconnect.models import User, Portfolio, Asset

portfolio_blueprint = Blueprint('portfolio', __name__)

@portfolio_blueprint.route('/portfolio', methods=['GET'])
def portfolio_index():
    """
    Display the portfolio index page.

    :return: Portfolio index page
    """
    portfolios = Portfolio.query.all()
    return render_template('portfolio/index.html', portfolios[portfolios])

@portfolio_blueprint.route('/portfolio/create', methods=['GET', 'POST'])
def create_portfolio():
    """
    Create a new portfolio.

    :return: Redirect to portfolio index page
    """
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        user_id = request.user.id
        portfolio = Portfolio(name=name, description=description, user_id=user_id)
        db.session.add(portfolio)
        db.session.commit()
        return redirect(url_for('portfolio.portfolio_index'))
    return render_template('portfolio/create.html')

@portfolio_blueprint.route('/portfolio/<int:portfolio_id>', methods=['GET'])
def view_portfolio(portfolio_id):
    """
    View a portfolio.

    :param portfolio_id: Portfolio ID
    :return: Portfolio page
    """
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    assets = Asset.query.filter_by(portfolio_id=portfolio_id).all()
    return render_template('portfolio/portfolio.html', portfolio=portfolio, assets=assets)
