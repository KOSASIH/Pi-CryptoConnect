# src/data/postprocessing.py
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class DataPostprocessor:
    def __init__(self, data, model_name, tokenizer_name):
        self.data = data
        self.model_name = model_name
        self.tokenizer_name = tokenizer_name
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def split_data(self):
        X = self.data.drop('label', axis=1)
        y = self.data['label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def evaluate_model(self, y_pred):
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        matrix = confusion_matrix(y_test, y_pred)
        return accuracy, report, matrix

    def generate_predictions(self, X_test):
        predictions = self.model.predict(X_test)
        return predictions

    def postprocess(self):
        X_train, X_test, y_train, y_test = self.split_data()
        predictions = self.generate_predictions(X_test)
        accuracy, report, matrix = self.evaluate_model(predictions)
        return accuracy, report, matrix
