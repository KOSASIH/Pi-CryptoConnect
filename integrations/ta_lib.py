import talib
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """A class to calculate technical indicators using TA-Lib."""

    def __init__(self, data: pd.DataFrame):
        """Initialize the TechnicalIndicators with the provided data.

        Args:
            data (pd.DataFrame): Pandas DataFrame containing OHLCV data.
        """
        self.data = data

    def calculate_indicators(self):
        """
        Calculate technical indicators using TA-Lib.

        :return: Dictionary with calculated indicators
        """
        indicators = {}
        try:
            # Calculate RSI
            indicators['RSI'] = talib.RSI(self.data['Close'])
            logger.info("RSI calculated successfully.")

            # Calculate MACD
            macd, macd_signal, macd_hist = talib.MACD(self.data['Close'])
            indicators['MACD'] = {
                'macd': macd,
                'signal': macd_signal,
                'hist': macd_hist
            }
            logger.info("MACD calculated successfully.")

            # Calculate Bollinger Bands
            upperband, middleband, lowerband = talib.BBANDS(self.data['Close'])
            indicators['Bollinger Bands'] = {
                'upperband': upperband,
                'middleband': middleband,
                'lowerband': lowerband
            }
            logger.info("Bollinger Bands calculated successfully.")

        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            raise

        return indicators

# Example usage
if __name__ == "__main__":
    # Sample OHLCV DataFrame
    data = pd.DataFrame({
        'Open': [100, 102, 101, 105, 107],
        'High': [102, 103, 106, 108, 110],
        'Low': [99, 100, 100, 104, 106],
        'Close': [101, 102, 105, 107, 109],
        'Volume': [1000, 1500, 2000, 2500, 3000]
    })

    indicators_calculator = TechnicalIndicators(data)
    indicators = indicators_calculator.calculate_indicators()

    # Display calculated indicators
    for key, value in indicators.items():
        print(f"{key}: {value}")
