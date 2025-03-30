import pandas as pd
import numpy as np
import logging
from pi_cryptoconnect.database import db
from pi_cryptoconnect.models import Strategy, Trade

class Simulator:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
        self.trades = []
        self.metrics = {}

    def run_simulation(self, start_date: str, end_date: str) -> None:
        """
        Run the simulation for the given strategy and time period.

        :param start_date: Start date of the simulation
        :param end_date: End date of the simulation
        :return: None
        """
        logging.info(f"Running simulation for strategy: {self.strategy.name} from {start_date} to {end_date}")

        # Load historical data for the given time period
        data = self.load_historical_data(start_date, end_date)

        # Iterate through the data and generate trades based on the strategy
        for index, row in data.iterrows():
            trade = self.generate_trade(row)
            if trade:
                self.trades.append(trade)

        # Calculate simulation metrics
        self.calculate_simulation_metrics()

    def load_historical_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Load historical data for the given time period.

        :param start_date: Start date of the simulation
        :param end_date: End date of the simulation
        :return: Historical data
        """
        try:
            data = pd.read_sql_table('historical_data', db.engine)
            data['date'] = pd.to_datetime(data['date'])  # Ensure date is in datetime format
            data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
            logging.info(f"Loaded {len(data)} rows of historical data.")
            return data
        except Exception as e:
            logging.error(f"Error loading historical data: {e}")
            raise

    def generate_trade(self, row: pd.Series) -> Trade:
        """
        Generate a trade based on the strategy and historical data.

        :param row: Historical data row
        :return: Trade object
        """
        # Implement strategy logic to generate trades
        # Example: Buy if the closing price is above a certain threshold
        if row['close'] > self.strategy.entry_threshold:
            trade = Trade(
                date=row['date'],
                type='buy',
                asset=self.strategy.asset,
                quantity=self.strategy.position_size,
                entry_price=row['close']
            )
            logging.info(f"Generated trade: {trade}")
            return trade
        return None

    def calculate_simulation_metrics(self) -> None:
        """
        Calculate simulation metrics (e.g. profit/loss, Sharpe ratio, etc.).

        :return: None
        """
        if not self.trades:
            logging.warning("No trades were generated during the simulation.")
            return

        # Calculate profit/loss for each trade
        total_profit_loss = 0
        for trade in self.trades:
            total_profit_loss += trade.exit_price - trade.entry_price  # Simplified for demonstration

        self.metrics['profit_loss'] = total_profit_loss
        self.metrics['sharpe_ratio'] = self.calculate_sharpe_ratio()
        self.metrics['sortino_ratio'] = self.calculate_sortino_ratio()
        self.metrics['max_drawdown'] = self.calculate_max_drawdown()

        logging.info(f"Simulation Metrics: {self.metrics}")

    def calculate_sharpe_ratio(self) -> float:
        """
        Calculate the Sharpe Ratio.

        :return: Sharpe Ratio
        """
        # Implement Sharpe Ratio calculation logic
        returns = [trade.exit_price - trade.entry_price for trade in self.trades]
        mean_return = np.mean(returns)
        std_dev = np.std(returns)
        if std_dev == 0:
            return 0
        return mean_return / std_dev

    def calculate_sortino_ratio(self) -> float:
        """
        Calculate the Sortino Ratio.

        :return: Sortino Ratio
        """
        # Implement Sortino Ratio calculation logic
        returns = [trade.exit_price - trade.entry_price for trade in self.trades]
        downside_returns = [r for r in returns if r < 0]
        mean_return = np.mean(returns)
        downside_deviation = np.std(downside_returns) if downside_returns else 0
        if downside_deviation == 0:
            return 0
        return mean_return / downside_deviation

    def calculate_max_drawdown(self) -> float:
        """
        Calculate the maximum drawdown.

        :return: Maximum Drawdown
        """
        # Implement Maximum Drawdown calculation logic
        cumulative_returns = np.cumsum([trade.exit_price - trade.entry_price for trade in self.trades])
        peak = cumulative_returns[0]
        max_drawdown = 0
        for value in cumulative_returns:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            max_drawdown = max(max_drawdown, drawdown)
        return max_drawdown
