import pandas as pd
from scipy.optimize import minimize
from pi_cryptoconnect.database import db
from pi_cryptoconnect.models import Portfolio, Asset

def optimize_portfolio(portfolio_id: int) -> None:
    """
    Optimize a portfolio using mean-variance optimization.

    :param portfolio_id: Portfolio ID
    :return: None
    """
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    assets = Asset.query.filter_by(portfolio_id=portfolio_id).all()

    # Calculate asset returns and covariance matrix
    returns = pd.DataFrame([asset.return_ for asset in assets])
    cov_matrix = returns.cov()

    # Define optimization function
    def optimization_function(weights):
        portfolio_return = np.sum(returns.mean() * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -portfolio_return / portfolio_volatility

    # Define constraints
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # Run optimization
    result = minimize(optimization_function, np.array([1.0 / len(assets)] * len(assets)), method='SLSQP', constraints=constraints)

    # Update asset quantities
    for i, asset in enumerate(assets):
        asset.quantity = int(result.x[i] * portfolio.total_value)
    db.session.commit()
