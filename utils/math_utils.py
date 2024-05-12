# utils/math_utils.py
from typing import List, Tuple

import numpy as np


def calculate_moving_average(data: List[float], window_size: int) -> List[float]:
    return np.convolve(data, np.ones(window_size), "valid") / window_size


def calculate_exponential_moving_average(
    data: List[float], alpha: float
) -> List[float]:
    ema = [0.0] * len(data)
    ema[0] = data[0]
    for i in range(1, len(data)):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]
    return ema


def calculate_standard_deviation(data: List[float]) -> float:
    mean = np.mean(data)
    variance = np.var(data)
    return np.sqrt(variance)


def calculate_correlation(x: List[float], y: List[float]) -> float:
    covariance = np.cov(x, y)[0][1]
    std_x = np.std(x)
    std_y = np.std(y)
    return covariance / (std_x * std_y)


def calculate_linear_regression(x: List[float], y: List[float]) -> Tuple[float, float]:
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    intercept = y_mean - slope * x_mean
    return slope, intercept
