from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from pi_cryptoconnect.database import db
from pi_cryptoconnect.models import User, Strategy
from wtforms import Form, StringField, TextAreaField, validators

marketplace_blueprint = Blueprint('marketplace', __name__)

class StrategyForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=100)])
    description = TextAreaField('Description', [validators.Length(min=1)])
    code = TextAreaField('Code', [validators.Length(min=1)])

@marketplace_blueprint.route('/marketplace', methods=['GET'])
def marketplace_index():
    """
    Display the marketplace index page with pagination.

    :return: Marketplace index page
    """
    page = request.args.get('page', 1, type=int)
    strategies = Strategy.query.paginate(page, per_page=10)  # 10 strategies per page
    return render_template('marketplace/index.html', strategies=strategies)

@marketplace_blueprint.route('/marketplace/create', methods=['GET', 'POST'])
@login_required
def create_strategy():
    """
    Create a new trading strategy.

    :return: Redirect to marketplace index page
    """
    form = StrategyForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        description = form.description.data
        code = form.code.data
        user_id = current_user.id
        strategy = Strategy(name=name, description=description, code=code, user_id=user_id)
        db.session.add(strategy)
        db.session.commit()
        flash('Strategy created successfully!', 'success')
        return redirect(url_for('marketplace.marketplace_index'))
    return render_template('marketplace/create.html', form=form)

@marketplace_blueprint.route('/marketplace/<int:strategy_id>', methods=['GET'])
def view_strategy(strategy_id):
    """
    View a trading strategy.

    :param strategy_id: Strategy ID
    :return: Strategy page
    """
    strategy = Strategy.query.get_or_404(strategy_id)
    return render_template('marketplace/strategy.html', strategy=strategy)

@marketplace_blueprint.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors.

    :param error: Error object
    :return: 404 error page
    """
    return render_template('404.html'), 404

@marketplace_blueprint.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors.

    :param error: Error object
    :return: 500 error page
    """
    db.session.rollback()  # Rollback the session on error
    return render_template('500.html'), 500
