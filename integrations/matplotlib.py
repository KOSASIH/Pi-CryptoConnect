import matplotlib.pyplot as plt
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChartPlotter:
    """A class to plot charts using Matplotlib."""

    def __init__(self, data: pd.DataFrame):
        """Initialize the ChartPlotter with the provided data.

        Args:
            data (pd.DataFrame): Pandas DataFrame containing OHLCV data.
        """
        self.data = data

    def plot_line_chart(self, title: str, xlabel: str = 'Time', ylabel: str = 'Price', save_path: str = None):
        """Plot a line chart for the 'Close' prices.

        Args:
            title (str): The title of the chart.
            xlabel (str): The label for the x-axis.
            ylabel (str): The label for the y-axis.
            save_path (str, optional): Path to save the chart image. If None, the chart will be displayed.
        """
        try:
            plt.figure(figsize=(12, 6))
            plt.plot(self.data['Close'], label='Close Price', color='blue', linewidth=2)
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.legend()
            plt.grid(True)

            if save_path:
                plt.savefig(save_path, bbox_inches='tight')
                logger.info(f"Chart saved to {save_path}.")
            else:
                plt.show()
        except Exception as e:
            logger.error(f"Error plotting line chart: {e}")
            raise
        finally:
            plt.close()  # Close the figure to free memory

    def plot_candlestick_chart(self, title: str, save_path: str = None):
        """Plot a candlestick chart for the OHLC data.

        Args:
            title (str): The title of the chart.
            save_path (str, optional): Path to save the chart image. If None, the chart will be displayed.
        """
        try:
            from mplfinance import candlestick_ohlc
            import matplotlib.dates as mdates

            # Prepare data for candlestick chart
            self.data['Date'] = mdates.date2num(self.data.index.to_pydatetime())
            ohlc_data = self.data[['Date', 'Open', 'High', 'Low', 'Close']].values

            plt.figure(figsize=(12, 6))
            ax = plt.gca()
            candlestick_ohlc(ax, ohlc_data, width=0.6, colorup='green', colordown='red')
            plt.title(title)
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.grid(True)

            if save_path:
                plt.savefig(save_path, bbox_inches='tight')
                logger.info(f"Candlestick chart saved to {save_path}.")
            else:
                plt.show()
        except Exception as e:
            logger.error(f"Error plotting candlestick chart: {e}")
            raise
        finally:
            plt.close()  # Close the figure to free memory

# Example usage
if __name__ == "__main__":
    # Sample OHLCV DataFrame
    data = pd.DataFrame({
        'Open': [100, 102, 101, 105, 107],
        'High': [102, 103, 106, 108, 110],
        'Low': [99, 100, 100, 104, 106],
        'Close': [101, 102, 105, 107, 109]
    }, index=pd.date_range(start='2023-01-01', periods=5, freq='D'))

    plotter = ChartPlotter(data)
    plotter.plot_line_chart(title='Sample Line Chart')
    plotter.plot_candlestick_chart(title='Sample Candlestick Chart')
