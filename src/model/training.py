# src/model/training.py
import torch
import torch.nn as nn
import torch.optim as optim
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from src.data import DataPreprocessor


class ModelTrainer:
    def __init__(
        self,
        model_name,
        tokenizer_name,
        train_data_path,
        val_data_path,
        batch_size,
        learning_rate,
        num_epochs,
    ):
        self.model_name = model_name
        self.tokenizer_name = tokenizer_name
        self.train_data_path = train_data_path
        self.val_data_path = val_data_path
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.preprocessor = DataPreprocessor(
            self.train_data_path, self.tokenizer_name, self.model_name
        )

    def preprocess_data(self):
        self.train_data = self.preprocessor.preprocess()
        self.val_data = self.preprocessor.preprocess()

    def create_data_loader(self, data, batch_size):
        tensor_data = torch.tensor(data)
        data_loader = torch.utils.data.DataLoader(
            tensor_data, batch_size=batch_size, shuffle=True
        )
        return data_loader

    def train(self):
        self.preprocess_data()
        train_loader = self.create_data_loader(self.train_data, self.batch_size)
        val_loader = self.create_data_loader(self.val_data, self.batch_size)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        for epoch in range(self.num_epochs):
            self.model.train()
            for batch in train_loader:
                optimizer.zero_grad()
                input_ids = batch[:, 0].long()
                attention_mask = batch[:, 1].long()
                labels = batch[:, 2].long()
                outputs = self.model(
                    input_ids, attention_mask=attention_mask, labels=labels
                )
                loss = outputs.loss
                loss.backward()
                optimizer.step()
            self.model.eval()
            with torch.no_grad():
                total_val_loss = 0
                total_val_correct = 0
                for batch in val_loader:
                    input_ids = batch[:, 0].long()
                    attention_mask = batch[:, 1].long()
                    labels = batch[:, 2].long()
                    outputs = self.model(
                        input_ids, attention_mask=attention_mask, labels=labels
                    )
                    loss = outputs.loss
                    logits = outputs.logits
                    predicted = torch.argmax(logits, dim=1)
                    total_val_loss += loss.item()
                    total_val_correct += (predicted == labels).sum().item()
                val_accuracy = total_val_correct / len(self.val_data)
                print(
                    f"Epoch {epoch+1}/{self.num_epochs}, Val Loss: {total_val_loss:.4f}, Val Accuracy: {val_accuracy:.4f}"
                )
