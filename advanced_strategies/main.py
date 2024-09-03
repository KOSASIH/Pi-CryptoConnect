import pandas as pd
import numpy as np
from utils.data_loader import DataLoader
from utils.feature_engineering import FeatureEngineering
from trading_simulator import TradingSimulator
from metrics import Metrics

def main():
    # Load data
    data_loader = DataLoader(file_path="data/crypto_data.csv", target_column="Close")
    X_train_scaled, X_test_scaled, y_train, y_test = data_loader.load_and_split_data()

    # Engineer features
    feature_engineering = FeatureEngineering(data=X_train_scaled, target_column="Close")
    engineered_data = feature_engineering.engineer_features()

    # Define trading strategy
    def trading_strategy(data):
        # Simple moving average strategy
        short_window = 20
        long_window = 50
        signal = 0
        if data["Close"] > data["MA_" + str(long_window)] and data["Close"] > data["MA_" + str(short_window)]:
            signal = 1  # Long signal
        elif data["Close"] < data["MA_" + str(long_window)] and data["Close"] < data["MA_" + str(short_window)]:
            signal = -1  # Short signal
        return signal

    # Simulate trading
    trading_simulator = TradingSimulator(data=engineered_data, trading_strategy=trading_strategy)
    trading_simulator.simulate_trading()

    # Calculate metrics
    metrics = Metrics(y_true=y_test, y_pred=trading_simulator.equity_curve)
    metrics_dict = metrics.calculate_all_metrics()
    print("Metrics:")
    for key, value in metrics_dict.items():
        print(f"{key}: {value:.4f}")

    # Plot equity curve
    trading_simulator.plot_equity_curve()

if __name__ == "__main__":
    main()
