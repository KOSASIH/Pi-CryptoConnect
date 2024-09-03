import pandas as pd
import numpy as np
from metrics import Metrics

class TradingSimulator:
    def __init__(self, data, trading_strategy, initial_capital=10000):
        self.data = data
        self.trading_strategy = trading_strategy
        self.initial_capital = initial_capital
        self.position_size = 0
        self.cash = initial_capital
        self.equity_curve = [initial_capital]

    def simulate_trading(self):
        for i in range(len(self.data)):
            signal = self.trading_strategy(self.data.iloc[i])
            if signal == 1:  # Long signal
                self.position_size = self.cash / self.data.iloc[i]["Close"]
                self.cash = 0
            elif signal == -1:  # Short signal
                self.position_size = -self.cash / self.data.iloc[i]["Close"]
                self.cash = 0
            else:  # No signal
                self.position_size = 0
                self.cash = self.equity_curve[-1]
            self.equity_curve.append(self.position_size * self.data.iloc[i]["Close"] + self.cash)

    def calculate_metrics(self):
        metrics = Metrics(self.data["Close"], self.equity_curve)
        return metrics.calculate_all_metrics()

    def plot_equity_curve(self):
        import matplotlib.pyplot as plt
        plt.plot(self.equity_curve)
        plt.xlabel("Time")
        plt.ylabel("Equity")
        plt.title("Equity Curve")
        plt.show()
