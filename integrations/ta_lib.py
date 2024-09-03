import talib

def calculate_indicators(data):
    """
    Calculate technical indicators using TA-Lib.

    :param data: Pandas DataFrame with OHLCV data
    :return: Dictionary with calculated indicators
    """
    indicators = {}
    indicators['RSI'] = talib.RSI(data['Close'])
    indicators['MACD'] = talib.MACD(data['Close'])
    indicators['Bollinger Bands'] = talib.BBANDS(data['Close'])
    return indicators
