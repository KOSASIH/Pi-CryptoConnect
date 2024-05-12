# src/model/inference.py
import torch
import torch.nn as nn
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from src.data import DataPreprocessor


class ModelInferencer:
    def __init__(self, model_name, tokenizer_name, test_data_path, batch_size):
        self.model_name = model_name
        self.tokenizer_name = tokenizer_name
        self.test_data_path = test_data_path
        self.batch_size = batch_size
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.preprocessor = DataPreprocessor(
            self.test_data_path, self.tokenizer_name, self.model_name
        )

    def preprocess_data(self):
        self.test_data = self.preprocessor.preprocess()

    def create_data_loader(self, data, batch_size):
        tensor_data = torch.tensor(data)
        data_loader = torch.utils.data.DataLoader(
            tensor_data, batch_size=batch_size, shuffle=False
        )
        return data_loader

    def infer(self):
        self.preprocess_data()
        test_loader = self.create_data_loader(self.test_data, self.batch_size)
        self.model.eval()
        with torch.no_grad():
            total_correct = 0
            for batch in test_loader:
                input_ids = batch[:, 0].long()
                attention_mask = batch[:, 1].long()
                labels = batch[:, 2].long()
                outputs = self.model(input_ids, attention_mask=attention_mask)
                logits = outputs.logits
                predicted = torch.argmax(logits, dim=1)
                total_correct += (predicted == labels).sum().item()
            accuracy = total_correct / len(self.test_data)
            print(f"Test Accuracy: {accuracy:.4f}")
