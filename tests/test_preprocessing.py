import unittest

from src.preprocessing import preprocess_data


class TestPreprocessing(unittest.TestCase):
    def test_preprocess_data(self):
        raw_data = [
            {"text": "Hello, world!", "label": "POSITIVE"},
            {"text": "This is a negative sentence.", "label": "NEGATIVE"},
        ]

        expected_data = [
            {
                "input_ids": [101, 1453, 1039, 102],
                "attention_mask": [1, 1, 1, 1],
                "label": 1,
            },
            {
                "input_ids": [101, 1339, 1828, 1478, 1037, 102],
                "attention_mask": [1, 1, 1, 1, 1, 1],
                "label": 0,
            },
        ]

        self.assertEqual(preprocess_data(raw_data), expected_data)


if __name__ == "__main__":
    unittest.main()
