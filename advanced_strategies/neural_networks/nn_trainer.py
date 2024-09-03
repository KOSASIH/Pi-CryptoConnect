import numpy as np
import pandas as pd
from nn_model import NnModel

class NnTrainer:
    def __init__(self, model, data, labels):
        self.model = model
        self.data = data
        self.labels = labels

    def train(self, epochs=100, batch_size=32, validation_split=0.2, early_stopping_patience=5, reduce_lr_patience=5):
        self.model.train(self.data, self.labels, epochs=epochs, batch_size=batch_size, validation_split=validation_split, early_stopping_patience=early_stopping_patience, reduce_lr_patience=reduce_lr_patience)

    def predict(self, data):
        return self.model.predict(data)

    def evaluate(self, data, labels):
        return self.model.model.evaluate(data, labels)

    def save(self, filename):
        self.model.save(filename)

    def load(self, filename):
        self.model.load(filename)
