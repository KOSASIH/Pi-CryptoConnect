import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class DataLoader:
    def __init__(self, file_path, target_column, test_size=0.2, random_state=42):
        self.file_path = file_path
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state

    def load_data(self):
        data = pd.read_csv(self.file_path)
        X = data.drop(self.target_column, axis=1)
        y = data[self.target_column]
        return X, y

    def split_data(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=self.random_state)
        return X_train, X_test, y_train, y_test

    def scale_data(self, X_train, X_test):
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled

    def load_and_split_data(self):
        X, y = self.load_data()
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        X_train_scaled, X_test_scaled = self.scale_data(X_train, X_test)
        return X_train_scaled, X_test_scaled, y_train, y_test
