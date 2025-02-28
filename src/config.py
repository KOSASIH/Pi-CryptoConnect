# src/config.py

import json
import os

class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.settings = self.load_config()

    def load_config(self):
        """Load configuration from a JSON file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return self.default_config()

    def default_config(self):
        """Return default configuration settings."""
        return {
            "model_name": "default_model",
            "tokenizer_name": "default_tokenizer",
            "train_data_path": "./data/train.json",
            "val_data_path": "./data/val.json",
            "test_data_path": "./data/test.json",
            "batch_size": 32,
            "learning_rate": 1e-5,
            "num_epochs": 3,
            "log_level": "INFO"
        }

    def save_config(self):
        """Save the current settings to a JSON file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key, default=None):
        """Get a configuration value by key."""
        return self.settings.get(key, default)

    def set(self, key, value):
        """Set a configuration value by key."""
        self.settings[key] = value
        self.save_config()

    def validate(self):
        """Validate configuration settings."""
        if not isinstance(self.settings.get("batch_size"), int) or self.settings["batch_size"] <= 0:
            raise ValueError("Batch size must be a positive integer.")
        if not isinstance(self.settings.get("learning_rate"), (float, int)) or self.settings["learning_rate"] <= 0:
            raise ValueError("Learning rate must be a positive number.")
        if not isinstance(self.settings.get("num_epochs"), int) or self.settings["num_epochs"] <= 0:
            raise ValueError("Number of epochs must be a positive integer.")
        if not isinstance(self.settings.get("log_level"), str):
            raise ValueError("Log level must be a string.")

    def print_config(self):
        """Print the current configuration settings."""
        print(json.dumps(self.settings, indent=4))

# Example usage
if __name__ == "__main__":
    config = Config()
    config.print_config()
    try:
        config.validate()
        print("Configuration is valid.")
    except ValueError as e:
        print(f"Configuration error: {e}")
