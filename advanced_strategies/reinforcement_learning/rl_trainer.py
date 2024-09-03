import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam
from rl.core import Trainer
from rl.memory import Memory
from rl.experience import Experience

class RlTrainer(Trainer):
    def __init__(self, agent, environment, memory_size=10000, batch_size=32, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        super(RlTrainer, self).__init__()
        self.agent = agent
        self.environment = environment
        self.memory = Memory(memory_size)
        self.batch_size = batch_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

    def train(self, episodes=1000):
        for episode in range(episodes):
            state = self.environment.reset()
            done = False
            rewards = 0
            while not done:
                action = self.agent.act(state)
                next_state, reward, done, _ = self.environment.step(action)
                experience = Experience(state, action, reward, next_state, done)
                self.memory.add(experience)
                state = next_state
                rewards += reward
            self.update_agent()
            print(f"Episode {episode+1}, Reward: {rewards}, Epsilon: {self.epsilon:.2f}")

    def update_agent(self):
        batch = self.memory.sample(self.batch_size)
        states = np.array([experience.state for experience in batch])
        actions = np.array([experience.action for experience in batch])
        rewards = np.array([experience.reward for experience in batch])
        next_states = np.array([experience.next_state for experience in batch])
        dones = np.array([experience.done for experience in batch])

        targets = rewards + self.gamma * np.amax(self.agent.target_model.predict(next_states), axis=1) * (1 - dones)
        targets = targets.reshape(-1, 1)

        self.agent.model.fit(states, targets, epochs=1, verbose=0)
        self.agent.update_target_model()
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)

    def save(self, filename):
        self.agent.save(filename)

    def load(self, filename):
        self.agent.load(filename)
