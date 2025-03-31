import numpy as np
import pandas as pd
from scipy.optimize import minimize
from pi_cryptoconnect.database import db
from pi_cryptoconnect.models import Portfolio, Asset

def calculate_asset_returns(assets):
    """
    Calculate historical returns for each asset.

    :param assets: List of Asset objects
    :return: DataFrame of asset returns
    """
    returns_data = []
    for asset in assets:
        # Fetch historical price data for the asset (this is a placeholder)
        historical_prices = fetch_historical_prices(asset.symbol)
        if historical_prices is not None and len(historical_prices) > 1:
            returns = historical_prices.pct_change().dropna()
            returns_data.append(returns)
        else:
            print(f"Insufficient data for asset: {asset.symbol}")
            returns_data.append(pd.Series([0]))  # Append zero returns if data is insufficient

    return pd.DataFrame(returns_data).T

def fetch_historical_prices(symbol):
    """
    Fetch historical prices for a given asset symbol from a market data API.

    :param symbol: Asset symbol
    :return: List of historical prices
    """
    try:
        # Example API call (replace with a real API endpoint)
        response = requests.get(f'https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency=usd&days=30')
        if response.status_code == 200:
            prices = [price[1] for price in response.json()['prices']]
            return prices
        else:
            print(f"Error fetching historical prices for {symbol}: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def optimize_portfolio(portfolio_id: int) -> None:
    """
    Optimize a portfolio using mean-variance optimization.

    :param portfolio_id: Portfolio ID
    :return: None
    """
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    assets = Asset.query.filter_by(portfolio_id=portfolio_id).all()

    # Calculate asset returns
    returns = calculate_asset_returns(assets)
    if returns.empty:
        print("No returns data available for optimization.")
        return

    # Calculate covariance matrix
    cov_matrix = returns.cov()

    # Define optimization function
    def optimization_function(weights):
        portfolio_return = np.sum(returns.mean() * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -portfolio_return / portfolio_volatility  # Minimize negative Sharpe ratio

    # Define constraints
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(len(assets)))  # Weights must be between 0 and 1

    # Initial guess
    initial_weights = np.array([1.0 / len(assets)] * len(assets))

    # Run optimization
    result = minimize(optimization_function, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)

    if result.success:
        # Update asset quantities based on optimized weights
        for i, asset in enumerate(assets):
            asset.quantity = int(result.x[i] * portfolio.total_value())
        db.session.commit()
        print("Portfolio optimized successfully.")
    else:
        print("Optimization failed:", result.message)
