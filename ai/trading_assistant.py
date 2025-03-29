import pandas as pd
import numpy as np
import logging
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import talib
from pi_cryptoconnect.integrations.ta_lib import calculate_indicators
from pi_cryptoconnect.integrations.zipline import run_backtest
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TradingAssistant:
    def __init__(self, data=None, model_path=None):
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

        # Hyperparameter tuning
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        }
        grid_search = GridSearchCV(self.model, param_grid, cv=3, scoring='accuracy')
        grid_search.fit(X_train_scaled, y_train)
        self.model = grid_search.best_estimator_

        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info(f'Model accuracy: {accuracy:.3f}')
        logging.info(f'Classification report:\n{classification_report(y_test, y_pred)}')
        logging.info(f'Confusion matrix:\n{confusion_matrix(y_test, y_pred)}')
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

    def visualize_trading_opportunities(self, opportunities):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['Close'], label='Close Price', color='blue')
        plt.scatter(opportunities.index, opportunities['Close'], label='Buy Signal', marker='^', color='green')
        plt.title('Trading Opportunities')
        plt.legend()
        plt.show()

def load_market_data(tickers, start_date, end_date):
    data = pd.DataFrame()
    for ticker in tickers:
        try:
            data[ticker] = yf.download(ticker, start=start_date, end=end_date)['Close']
        except Exception as e:
            logging.error(f"Error loading data for {ticker}: {e}")
    return data

def calculate_indicators(data):
    indicators = pd.DataFrame()
    indicators['RSI'] = talib.RSI(data['Close'])
    indicators['MAC D'] = talib.MACD(data['Close'])['macd']
    indicators['Bollinger_Upper'], indicators['Bollinger_Middle'], indicators['Bollinger_Lower'] = talib.BBANDS(data['Close'])
    return indicators

class TradingStrategy:
    def __init__(self, data, model, name):
        self.data = data
        self.model = model
        self.name = name
        self.trades = []

    def generate_trades(self):
        opportunities = self.data[self.data['target'] == 1]
        for index, row in opportunities.iterrows():
            self.trades.append({'date': index, 'price': row['Close'], 'action': 'buy'})

    def evaluate_strategy(self):
        # Placeholder for strategy evaluation logic
        logging.info(f"Evaluating strategy: {self.name}")
        # Implement evaluation metrics here

# Example usage
if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT']
    start_date = '2022-01-01'
    end_date = '2023-01-01'
    
    trading_assistant = TradingAssistant()
    market_data = trading_assistant.analyze_market_data(tickers, start_date, end_date)
    trading_assistant.data = market_data
    trading_assistant.train_model()
    
    opportunities = trading_assistant.identify_trading_opportunities(market_data)
    trading_assistant.visualize_trading_opportunities(opportunities)
