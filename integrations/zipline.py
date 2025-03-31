import zipline
from zipline.api import order, record, symbol
import pandas as pd
import logging
from zipline.utils.run_algo import run_algorithm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Backtester:
    """A class to run backtests using Zipline."""

    def __init__(self, data: pd.DataFrame, start: str, end: str, capital_base: float = 10000):
        """
        Initialize the Backtester with the provided data and parameters.

        Args:
            data (pd.DataFrame): Pandas DataFrame containing OHLCV data.
            start (str): Start date for the backtest in 'YYYY-MM-DD' format.
            end (str): End date for the backtest in 'YYYY-MM-DD' format.
            capital_base (float): Initial capital for the backtest.
        """
        self.data = data
        self.start = start
        self.end = end
        self.capital_base = capital_base

    def run_backtest(self, strategy):
        """
        Run a backtest using Zipline.

        :param strategy: Zipline strategy function
        :return: Zipline backtest results
        """
        try:
            # Prepare the data for Zipline
            self.data['date'] = self.data.index
            self.data = self.data[['date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            self.data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
            self.data['datetime'] = pd.to_datetime(self.data['datetime'])
            self.data.set_index('datetime', inplace=True)

            # Run the backtest
            results = run_algorithm(
                start=self.start,
                end=self.end,
                initialize=strategy,
                capital_base=self.capital_base,
                data_frequency='daily',
                trading_calendar=zipline.utils.calendars.get_calendar('NYSE'),
                bundle='quantopian-quandl',  # Use a data bundle
                data=self.data
            )
            logger.info("Backtest completed successfully.")
            return results

        except Exception as e:
            logger.error(f"Error running backtest: {e}")
            raise

# Example strategy function
def initialize(context):
    context.asset = symbol('AAPL')

def handle_data(context, data):
    # Example strategy: Buy AAPL if not already owned
    if not context.portfolio.positions[context.asset].amount:
        order(context.asset, 10)  # Buy 10 shares
    record(AAPL=data.current(context.asset, 'price'))

# Example usage
if __name__ == "__main__":
    # Sample OHLCV DataFrame
    data = pd.DataFrame({
        'Open': [100, 102, 101, 105, 107],
        'High': [102, 103, 106, 108, 110],
        'Low': [99, 100, 100, 104, 106],
        'Close': [101, 102, 105, 107, 109],
        'Volume': [1000, 1500, 2000, 2500, 3000]
    }, index=pd.date_range(start='2023-01-01', periods=5, freq='D'))

    backtester = Backtester(data, start='2023-01-01', end='2023-01-05', capital_base=10000)
    results = backtester.run_backtest(initialize)

    # Display results
    print(results)
