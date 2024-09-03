import numpy as np
import pandas as pd
from nn_model import NnModel

class NnTrainer:
    def __init__(self, model, data, labels):
        self.model = model
        self.data = data
        self.labels = labels

    def train(self):
        self.model.train(self.data, self.labels)

    def predict(self, data):
        return self.model.predict(data)

    def evaluate(self, data, labels):
        return self.model.model.evaluate(data, labels)

    def save(self, filename):
        self.model.save(filename)

    def load(self, filename):
        self.model.load(filename)
