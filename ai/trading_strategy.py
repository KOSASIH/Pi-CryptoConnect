import pandas as pd
import numpy as np
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from pi_cryptoconnect.ai.feature_engineering import engineer_features
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TradingStrategy:
    def __init__(self, data, ticker, exchange):
        self.data = data
        self.ticker = ticker
        self.exchange = exchange

    def train_model(self):
        X = self.data.drop(['Target'], axis=1)
        y = self.data['Target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Hyperparameter tuning
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        }
        grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, scoring='accuracy')
        grid_search.fit(X_train, y_train)
        model = grid_search.best_estimator_

        y_pred = model.predict(X_test)
        logging.info("Model Performance:")
        logging.info("Accuracy: %.2f" % accuracy_score(y_test, y_pred))
        logging.info("Classification Report:\n%s" % classification_report(y_test, y_pred))
        logging.info("Confusion Matrix:\n%s" % confusion_matrix(y_test, y_pred))
        return model

    def generate_signals(self, model):
        signals = pd.DataFrame(index=self.data.index, columns=['Signal'])
        signals['Signal'] = 0
        for i in range(len(self.data)):
            row = self.data.iloc[i]
            if row['RSI'] < 30:
                signals.iloc[i]['Signal'] = 1  # Buy signal
            elif row['RSI'] > 70:
                signals.iloc[i]['Signal'] = -1  # Sell signal
            elif row['MACD'] > row['MACD Signal']:
                signals.iloc[i]['Signal'] = 1  # Buy signal
            elif row['MACD'] < row['MACD Signal']:
                signals.iloc[i]['Signal'] = -1  # Sell signal
        return signals

    def backtest_strategy(self, signals):
        portfolio = pd.DataFrame(index=self.data.index, columns=['Position', 'Cash', 'Value'])
        portfolio['Position'] = 0
        portfolio['Cash'] = 10000
        portfolio['Value'] = 10000

        for i in range(1, len(self.data)):
            row = self.data.iloc[i]
            signal = signals.iloc[i]['Signal']
            portfolio.iloc[i] = portfolio.iloc[i - 1]  # Carry forward previous values

            if signal == 1 and portfolio.iloc[i - 1]['Cash'] >= row['Close']:
                portfolio.iloc[i]['Position'] = portfolio.iloc[i - 1]['Position'] + 1
                portfolio.iloc[i]['Cash'] -= row['Close']
            elif signal == -1 and portfolio.iloc[i - 1]['Position'] > 0:
                portfolio.iloc[i]['Position'] = portfolio.iloc[i - 1]['Position'] - 1
                portfolio.iloc[i]['Cash'] += row['Close']

            portfolio.iloc[i]['Value'] = portfolio.iloc[i]['Cash'] + (portfolio.iloc[i]['Position'] * row['Close'])

        portfolio['Returns'] = portfolio['Value'].pct_change()
        return portfolio

    def visualize_performance(self, portfolio):
        plt.figure(figsize=(14, 7))
        plt.plot(portfolio['Value'], label='Portfolio Value', color='blue')
        plt.title(f'Portfolio Performance for {self.ticker}')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt .legend()
        plt.grid()
        plt.show()

def trading_strategy(data, ticker, exchange):
    trading_strategy = TradingStrategy(data, ticker, exchange)
    data = engineer_features(data)
    model = trading_strategy.train_model()
    signals = trading_strategy.generate_signals(model)
    portfolio = trading_strategy.backtest_strategy(signals)
    trading_strategy.visualize_performance(portfolio)
    return portfolio

# Example usage
if __name__ == "__main__":
    # Load your data here
    data = pd.read_csv('your_data.csv')  # Replace with your data source
    ticker = 'AAPL'
    exchange = 'NASDAQ'
    
    portfolio = trading_strategy(data, ticker, exchange)
