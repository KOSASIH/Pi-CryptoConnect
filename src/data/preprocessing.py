# src/data/preprocessing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.impute import SimpleImputer
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class DataPreprocessor:
    def __init__(self, data_path, tokenizer_name, model_name):
        self.data_path = data_path
        self.tokenizer_name = tokenizer_name
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def load_data(self):
        data = pd.read_csv(self.data_path)
        return data

    def preprocess_text(self, text_data):
        tokenized_data = self.tokenizer.batch_encode_plus(
            text_data,
            add_special_tokens=True,
            max_length=512,
            return_attention_mask=True,
            return_tensors='pt'
        )
        return tokenized_data

    def extract_features(self, tokenized_data):
        features = self.model(tokenized_data['input_ids'], attention_mask=tokenized_data['attention_mask'])
        return features.last_hidden_state[:, 0, :]

    def scale_data(self, data):
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        return scaled_data

    def reduce_dimensions(self, data):
        pca = PCA(n_components=0.95)
        reduced_data = pca.fit_transform(data)
        return reduced_data

    def select_features(self, data):
        selector = SelectKBest(k=10)
        selected_data = selector.fit_transform(data)
        return selected_data

    def impute_missing_values(self, data):
        imputer = SimpleImputer(strategy='mean')
        imputed_data = imputer.fit_transform(data)
        return imputed_data

    def preprocess(self):
        data = self.load_data()
        text_data = data['text']
        tokenized_data = self.preprocess_text(text_data)
        features = self.extract_features(tokenized_data)
        scaled_data = self.scale_data(features)
        reduced_data = self.reduce_dimensions(scaled_data)
        selected_data = self.select_features(reduced_data)
        imputed_data = self.impute_missing_values(selected_data)
        return imputed_data
