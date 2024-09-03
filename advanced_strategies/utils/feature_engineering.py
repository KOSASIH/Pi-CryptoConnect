import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import PolynomialFeatures

class FeatureEngineering:
    def __init__(self, data, target_column, num_features=10, poly_degree=2):
        self.data = data
        self.target_column = target_column
        self.num_features = num_features
        self.poly_degree = poly_degree

    def tfidf_transform(self, column):
        vectorizer = TfidfVectorizer(max_features=self.num_features)
        transformed_data = vectorizer.fit_transform(self.data[column])
        return pd.DataFrame(transformed_data.toarray(), columns=[f"{column}_{i}" for i in range(self.num_features)])

    def pca_transform(self, data):
        pca = PCA(n_components=self.num_features)
        transformed_data = pca.fit_transform(data)
        return pd.DataFrame(transformed_data, columns=[f"pca_{i}" for i in range(self.num_features)])

    def polynomial_transform(self, data):
        poly = PolynomialFeatures(degree=self.poly_degree)
        transformed_data = poly.fit_transform(data)
        return pd.DataFrame(transformed_data, columns=[f"poly_{i}" for i in range(transformed_data.shape[1])])

    def engineer_features(self):
        engineered_data = self.data.copy()
        for column in self.data.columns:
            if column != self.target_column:
                engineered_data = pd.concat([engineered_data, self.tfidf_transform(column)], axis=1)
                engineered_data = pd.concat([engineered_data, self.pca_transform(engineered_data[column])], axis=1)
                engineered_data = pd.concat([engineered_data, self.polynomial_transform(engineered_data[column])], axis=1)
        return engineered_data
