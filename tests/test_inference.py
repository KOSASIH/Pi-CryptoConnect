import unittest
from src.model.inference import infer_model

class TestInference(unittest.TestCase):
    def test_infer_model(self):
        model_name = 'distilbert-base-uncased'
        tokenizer_name = 'distilbert-base-uncased'
        test_data_path = 'tests/data/test.csv'
        batch_size = 32

        infer_model(model_name, tokenizer_name, test_data_path, batch_size)

        # Add additional assertions to test the inferred model

if __name__ == '__main__':
    unittest.main()
