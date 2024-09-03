import pandas as pd
import talib

def calculate_technical_indicators(data):
    indicators = pd.DataFrame()
    indicators['RSI'] = talib.RSI(data)
    indicators['MACD'] = talib.MACD(data)
    indicators['Bollinger Bands'] = talib.BBANDS(data)
    return indicators
