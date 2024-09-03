import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from pi_cryptoconnect.ai.feature_engineering import engineer_features

class TradingStrategy:
    def __init__(self, data, ticker, exchange):
        self.data = data
        self.ticker = ticker
        self.exchange = exchange

    def train_model(self):
        X = self.data.drop(['Target'], axis=1)
        y = self.data['Target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print("Model Performance:")
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        return model

    def generate_signals(self, model):
        signals = pd.DataFrame(index=self.data.index, columns=['Signal'])
        signals['Signal'] = 0
        for i in range(len(self.data)):
            row = self.data.iloc[i]
            if row['RSI'] < 30:
                signals.iloc[i]['Signal'] = 1
            elif row['RSI'] > 70:
                signals.iloc[i]['Signal'] = -1
            elif row['MACD'] > row['MACD Signal']:
                signals.iloc[i]['Signal'] = 1
            elif row['MACD'] < row['MACD Signal']:
                signals.iloc[i]['Signal'] = -1
        return signals

    def backtest_strategy(self, model, signals):
        portfolio = pd.DataFrame(index=self.data.index, columns=['Position', 'Cash', 'Value'])
        portfolio['Position'] = 0
        portfolio['Cash'] = 10000
        portfolio['Value'] = 10000
        for i in range(len(self.data)):
            row = self.data.iloc[i]
            signal = signals.iloc[i]['Signal']
            if signal == 1:
                portfolio.iloc[i]['Position'] = 1
                portfolio.iloc[i]['Cash'] -= row['Close']
                portfolio.iloc[i]['Value'] = portfolio.iloc[i-1]['Value'] + row['Close']
            elif signal == -1:
                portfolio.iloc[i]['Position'] = -1
                portfolio.iloc[i]['Cash'] += row['Close']
                portfolio.iloc[i]['Value'] = portfolio.iloc[i-1]['Value'] - row['Close']
        return portfolio

def trading_strategy(data, ticker, exchange):
    trading_strategy = TradingStrategy(data, ticker, exchange)
    data = engineer_features(data)
    model = trading_strategy.train_model()
    signals = trading_strategy.generate_signals(model)
    portfolio = trading_strategy.backtest_strategy(model, signals)
    return portfolio
