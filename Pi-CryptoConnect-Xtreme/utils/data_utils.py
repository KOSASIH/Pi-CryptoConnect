import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class DataUtils:
    @staticmethod
    def load_data(file_path):
        return pd.read_csv(file_path)

    @staticmethod
    def preprocess_data(data):
        scaler = MinMaxScaler()
        data[['feature1', 'feature2', 'feature3']] = scaler.fit_transform(data[['feature1', 'feature2', 'feature3']])
        return data

    @staticmethod
    def split_data(data, test_size=0.2):
        return data.split(test_size=test_size, random_state=42)

    @staticmethod
    def feature_engineering(data):
        # Implement feature engineering logic here
        pass

    @staticmethod
    def data_augmentation(data):
        # Implement data augmentation logic here
        pass
