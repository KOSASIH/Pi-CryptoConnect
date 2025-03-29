import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt
from talib import RSI, MACD, BBANDS, EMA, ATR
from pi_cryptoconnect.integrations.ta_lib import calculate_indicators

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FeatureEngineer:
    def __init__(self, data):
        self.data = data

    def handle_missing_values(self):
        logging.info("Handling missing values.")
        self.data.fillna(method='ffill', inplace=True)  # Forward fill
        self.data.fillna(method='bfill', inplace=True)  # Backward fill
        return self.data

    def calculate_technical_indicators(self):
        logging.info("Calculating technical indicators.")
        indicators = calculate_indicators(self.data)
        self.data = pd.concat([self.data, indicators], axis=1)
        return self.data

    def calculate_moving_averages(self):
        logging.info("Calculating moving averages.")
        self.data['MA_50'] = self.data['Close'].rolling(window=50).mean()
        self.data['MA_100'] = self.data['Close'].rolling(window=100).mean()
        self.data['MA_200'] = self.data['Close'].rolling(window=200).mean()
        return self.data

    def calculate_momentum_indicators(self):
        logging.info("Calculating momentum indicators.")
        self.data['RSI'] = RSI(self.data['Close'], timeperiod=14)
        self.data['MACD'], self.data['MACD_Signal'], _ = MACD(self.data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        self.data['Stochastic_Oscillator'] = (self.data['Close'] - self.data['Low'].rolling(window=14).min()) / (self.data['High'].rolling(window=14).max() - self.data['Low'].rolling(window=14).min())
        return self.data

    def calculate_volatility_indicators(self):
        logging.info("Calculating volatility indicators.")
        self.data['Bollinger_Upper'], self.data['Bollinger_Middle'], self.data['Bollinger_Lower'] = BBANDS(self.data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        self.data['ATR'] = ATR(self.data['High'], self.data['Low'], self.data['Close'], timeperiod=14)
        return self.data

    def normalize_features(self):
        logging.info("Normalizing features.")
        self.data = (self.data - self.data.mean()) / self.data.std()
        return self.data

    def visualize_indicators(self):
        logging.info("Visualizing indicators.")
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['Close'], label='Close Price', color='blue')
        plt.plot(self.data['MA_50'], label='50-Day MA', color='orange')
        plt.plot(self.data['MA_100'], label='100-Day MA', color='green')
        plt.plot(self.data['MA_200'], label='200-Day MA', color='red')
        plt.fill_between(self.data.index, self.data['Bollinger_Upper'], self.data['Bollinger_Lower'], color='lightgrey', label='Bollinger Bands')
        plt.title('Price and Moving Averages')
        plt.legend()
        plt.show()

    def engineer_features(self):
        self.data = self.handle_missing_values()
        self.data = self.calculate_technical_indicators()
        self.data = self.calculate_moving_averages()
        self.data = self.calculate_momentum_indicators()
        self.data = self.calculate_volatility_indicators()
        self.data = self.normalize_features()
        self.visualize_indicators()
        return self.data

def engineer_features(data):
    feature_engineer = FeatureEngineer(data)
    data = feature_engineer.engineer_features()
    return data

# Example usage
if __name__ == "__main__":
    # Sample data generation for demonstration
    dates = pd.date_range(start='2022- 01-01', end='2023-01-01', freq='B')
    data = pd.DataFrame(index=dates)
    data['Close'] = np.random.rand(len(dates)) * 100  # Simulated close prices
    data['High'] = data['Close'] + (np.random.rand(len(dates)) * 10)
    data['Low'] = data['Close'] - (np.random.rand(len(dates)) * 10)

    engineered_data = engineer_features(data)
    print(engineered_data)
