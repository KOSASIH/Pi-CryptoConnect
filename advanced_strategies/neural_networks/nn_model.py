import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam

class NnModel:
    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.model = self.create_model()

    def create_model(self):
        model = tf.keras.Sequential([
            LSTM(50, input_shape=(self.input_dim, 1)),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(self.output_dim, activation='linear')
        ])
        model.compile(loss='mse', optimizer=Adam(lr=0.001))
        return model

    def predict(self, data):
        return self.model.predict(data)

    def train(self, data, labels):
        self.model.fit(data, labels, epochs=100, batch_size=32, validation_split=0.2)

    def save(self, filename):
        self.model.save(filename)

    def load(self, filename):
        self.model.load_weights(filename)
