import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

class Metrics:
    def __init__(self, y_true, y_pred):
        self.y_true = y_true
        self.y_pred = y_pred

    def mean_squared_error(self):
        return mean_squared_error(self.y_true, self.y_pred)

    def mean_absolute_error(self):
        return mean_absolute_error(self.y_true, self.y_pred)

    def r2_score(self):
        return r2_score(self.y_true, self.y_pred)

    def annualized_return(self):
        return np.mean(self.y_pred) * np.sqrt(252)

    def annualized_volatility(self):
        return np.std(self.y_pred) * np.sqrt(252)

    def sharpe_ratio(self):
        return self.annualized_return() / self.annualized_volatility()

    def calculate_all_metrics(self):
        return {
            "Mean Squared Error": self.mean_squared_error(),
            "Mean Absolute Error": self.mean_absolute_error(),
            "R2 Score": self.r2_score(),
            "Annualized Return": self.annualized_return(),
            "Annualized Volatility": self.annualized_volatility(),
            "Sharpe Ratio": self.sharpe_ratio()
      }
