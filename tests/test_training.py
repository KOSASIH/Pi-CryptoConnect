import unittest
from src.model.training import train_model

class TestTraining(unittest.TestCase):
    def test_train_model(self):
        model_name = 'distilbert-base-uncased'
        tokenizer_name = 'distilbert-base-uncased'
        train_data_path = 'tests/data/train.csv'
        val_data_path = 'tests/data/val.csv'
        batch_size = 32
        learning_rate = 1e-5
        num_epochs = 3

        train_model(model_name, tokenizer_name, train_data_path, val_data_path, batch_size, learning_rate, num_epochs)

        # Add additional assertions to test the trained model

if __name__ == '__main__':
    unittest.main()
