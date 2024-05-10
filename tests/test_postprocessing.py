import unittest
from src.postprocessing import postprocess_predictions

class TestPostprocessing(unittest.TestCase):
    def test_postprocess_predictions(self):
        raw_predictions = [
            {'input_ids': [101, 1453, 1039, 102], 'predictions': [0.9, 0.1]},
            {'input_ids': [101, 1339, 1828, 1478, 1037, 102], 'predictions': [0.2, 0.8]}
        ]

        expected_predictions = [
            {'input_ids': [101, 1453, 1039, 102], 'label': 'POSITIVE'},
            {'input_ids': [101, 1339, 1828, 1478, 1037, 102], 'label': 'NEGATIVE'}
        ]

        self.assertEqual(postprocess_predictions(raw_predictions), expected_predictions)

if __name__ == '__main__':
    unittest.main()
