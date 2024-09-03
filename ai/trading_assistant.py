import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
import talib
import yfinance as yf
import numpy as np
from pi_cryptoconnect.integrations.ta_lib import calculate_indicators
from pi_cryptoconnect.integrations.zipline import run_backtest

class TradingAssistant:
    def __init__(self, data, model_path=None):
        self.data = data
        if model_path:
            self.model = joblib.load(model_path)
        else:
            self.model = RandomForestClassifier(n_estimators=100)
        self.scaler = StandardScaler()

    def train_model(self):
        X = self.data.drop(['target'], axis=1)
        y = self.data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.scaler.fit(X_train)
        X_train_scaled = self.scaler.transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        self.model.fit(X_train_scaled, y_train)
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Model accuracy: {accuracy:.3f}')
        print(f'Classification report:\n{classification_report(y_test, y_pred)}')
        print(f'Confusion matrix:\n{confusion_matrix(y_test, y_pred)}')
        joblib.dump(self.model, 'trading_assistant_model.joblib')

    def analyze_market_data(self, tickers, start_date, end_date):
        data = load_market_data(tickers, start_date, end_date)
        indicators = calculate_indicators(data)
        data = pd.concat([data, indicators], axis=1)
        data['target'] = np.where(data['Close'] > data['Close'].shift(1), 1, 0)
        return data

    def identify_trading_opportunities(self, data):
        X = data.drop(['target'], axis=1)
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        opportunities = data[predictions == 1]
        return opportunities

    def assist_strategy_creation(self, data, strategy_name):
        opportunities = self.identify_trading_opportunities(data)
        strategy = TradingStrategy(data, self.model, strategy_name)
        strategy.generate_trades()
        strategy.evaluate_strategy()
        return strategy

def load_market_data(tickers, start_date, end_date):
    data = pd.DataFrame()
    for ticker in tickers:
        data[ticker] = yf.download(ticker, start=start_date, end=end_date)['Close']
    return data

def calculate_indicators(data):
    indicators = pd.DataFrame()
    indicators['RSI'] = talib.RSI(data)
    indicators['MACD'] = talib.MACD(data)
    indicators['Bollinger Bands'] = talib.BBANDS(data)
    return indicators
