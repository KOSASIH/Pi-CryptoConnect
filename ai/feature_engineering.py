import pandas as pd
import numpy as np
from talib import RSI, MACD, BBANDS
from pi_cryptoconnect.integrations.ta_lib import calculate_indicators

class FeatureEngineer:
    def __init__(self, data):
        self.data = data

    def calculate_technical_indicators(self):
        indicators = calculate_indicators(self.data)
        self.data = pd.concat([self.data, indicators], axis=1)
        return self.data

    def calculate_moving_averages(self):
        self.data['MA_50'] = self.data['Close'].rolling(window=50).mean()
        self.data['MA_100'] = self.data['Close'].rolling(window=100).mean()
        self.data['MA_200'] = self.data['Close'].rolling(window=200).mean()
        return self.data

    def calculate_momentum_indicators(self):
        self.data['RSI'] = RSI(self.data['Close'], timeperiod=14)
        self.data['MACD'] = MACD(self.data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        self.data['Stochastic Oscillator'] = (self.data['Close'] - self.data['Low'].rolling(window=14).min()) / (self.data['High'].rolling(window=14).max() - self.data['Low'].rolling(window=14).min())
        return self.data

    def calculate_volatility_indicators(self):
        self.data['Bollinger Bands'] = BBANDS(self.data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        self.data['Average True Range'] = self.data['High'] - self.data['Low']
        return self.data

    def engineer_features(self):
        self.data = self.calculate_technical_indicators()
        self.data = self.calculate_moving_averages()
        self.data = self.calculate_momentum_indicators()
        self.data = self.calculate_volatility_indicators()
        return self.data

def engineer_features(data):
    feature_engineer = FeatureEngineer(data)
    data = feature_engineer.engineer_features()
    return data
