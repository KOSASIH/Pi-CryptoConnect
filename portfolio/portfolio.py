from flask import Blueprint, render_template, request, redirect, url_for, flash, session
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
    return render_template('portfolio/index.html', portfolios=portfolios)

@portfolio_blueprint.route('/portfolio/create', methods=['GET', 'POST'])
def create_portfolio():
    """
    Create a new portfolio.

    :return: Redirect to portfolio index page
    """
    if 'user_id' not in session:
        flash('You need to be logged in to create a portfolio.')
        return redirect(url_for('auth.login'))  # Redirect to login if not authenticated

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        user_id = session['user_id']  # Get user ID from session
        portfolio = Portfolio(name=name, description=description, user_id=user_id)
        
        try:
            db.session.add(portfolio)
            db.session.commit()
            flash('Portfolio created successfully!')
            return redirect(url_for('portfolio.portfolio_index'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash('Error creating portfolio: ' + str(e))

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
