import pandas as pd
import numpy as np
from gym.spaces import Box
from gym.envs.trading_env import TradingEnv

class RlEnvironment(TradingEnv):
    def __init__(self, data, window_size, commission=0.001):
        super(RlEnvironment, self).__init__()
        self.data = data
        self.window_size = window_size
        self.commission = commission
        self.state_dim = window_size * 5  # 5 features (open, high, low, close, volume)
        self.action_dim = 3  # buy, sell, hold
        self.observation_space = Box(low=-1, high=1, shape=(self.state_dim,))
        self.action_space = Box(low=-1, high=1, shape=(self.action_dim,))
        self.current_index = 0
        self.state = self.get_state(self.current_index)

    def reset(self):
        self.current_index = 0
        self.state = self.get_state(self.current_index)
        return self.state

    def step(self, action):
        self.current_index += 1
        next_state = self.get_state(self.current_index)
        reward = self.get_reward(action)
        done = self.is_done()
        return next_state, reward, done, {}

    def get_state(self, index):
        window_data = self.data.iloc[index:index + self.window_size]
        state = np.array([window_data['open'], window_data['high'], window_data['low'], window_data['close'], window_data['volume']])
        return state.flatten()

    def get_reward(self, action):
        if action == 0:  # buy
            reward = self.data.iloc[self.current_index + self.window_size]['close'] - self.data.iloc[self.current_index]['close']
        elif action == 1:  # sell
            reward = self.data.iloc[self.current_index]['close'] - self.data.iloc[self.current_index + self.window_size]['close']
        else:  # hold
            reward = 0
        reward -= self.commission
        return reward

    def is_done(self):
        return self.current_index >= len(self.data) - self.window_size

    def render(self, mode='human'):
        pass
