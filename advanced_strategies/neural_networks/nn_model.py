import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, LSTM, Dropout, Conv1D, MaxPooling1D, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l1_l2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

class NnModel:
    def __init__(self, input_dim, output_dim, hidden_layers=2, hidden_units=128, dropout_rate=0.2, l1_reg=0.01, l2_reg=0.01):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_layers = hidden_layers
        self.hidden_units = hidden_units
        self.dropout_rate = dropout_rate
        self.l1_reg = l1_reg
        self.l2_reg = l2_reg
        self.model = self.create_model()

    def create_model(self):
        model = tf.keras.Sequential()
        model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(self.input_dim, 1)))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Flatten())
        for _ in range(self.hidden_layers):
            model.add(Dense(self.hidden_units, activation='relu', kernel_regularizer=l1_l2(l1=self.l1_reg, l2=self.l2_reg)))
            model.add(Dropout(self.dropout_rate))
        model.add(Dense(self.output_dim, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=0.001), metrics=['mae'])
        return model

    def predict(self, data):
        return self.model.predict(data)

    def train(self, data, labels, epochs=100, batch_size=32, validation_split=0.2, early_stopping_patience=5, reduce_lr_patience=5):
        early_stopping = EarlyStopping(monitor='val_loss', patience=early_stopping_patience, min_delta=0.001)
        model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True, mode='min')
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', patience=reduce_lr_patience, min_delta=0.001, factor=0.5, min_lr=0.0001)
        self.model.fit(data, labels, epochs=epochs, batch_size=batch_size, validation_split=validation_split, callbacks=[early_stopping, model_checkpoint, reduce_lr])

    def save(self, filename):
        self.model.save(filename)

    def load(self, filename):
        self.model.load_weights(filename)
