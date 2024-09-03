import zipline

def run_backtest(strategy, data):
    """
    Run a backtest using Zipline.

    :param strategy: Zipline strategy function
    :param data: Pandas DataFrame with OHLCV data
    :return: Zipline backtest results
    """
    results = zipline.run_algorithm(strategy, data)
    return results
