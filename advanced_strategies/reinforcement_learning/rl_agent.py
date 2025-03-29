import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from rl.core import Agent

class RlAgent(Agent):
    def __init__(self, state_dim, action_dim, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        super(RlAgent, self).__init__()
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.model = self.create_model()
        self.target_model = self.create_model()
        self.update_target_model()

    def create_model(self):
        model = tf.keras.Sequential([
            LSTM(50, input_shape=(self.state_dim, 1)),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(self.action_dim, activation='linear')
        ])
        model.compile(loss='mse', optimizer=Adam(lr=0.001))
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_dim)
        else:
            state = np.array([state])
            return np.argmax(self.model.predict(state))

    def train(self, state, action, reward, next_state, done):
        state = np.array([state])
        next_state = np.array([next_state])
        target = self.model.predict(state)
        target[0, action] = reward
        if not done:
            target[0, action] += self.gamma * np.amax(self.target_model.predict(next_state)[0])
        self.model.fit(state, target, epochs=1, verbose=0)
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)

    def save(self, filename):
        self.model.save(filename)

    def load(self, filename):
        self.model.load_weights(filename)
        self.update_target_model()
