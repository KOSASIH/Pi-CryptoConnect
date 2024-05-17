import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
data = pd.read_csv('dataset.csv')

# Explore and clean the data
# (This step depends on the specific dataset and problem, so I'll assume that it's already been done)

# Prepare the data for modeling
X = data[['feature1', 'feature2', 'feature3']] # Select the relevant features
y = data['target'] # Select the target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a predictive model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print('Mean Squared Error:', mse)
print('R^2 Score:', r2)

# Use the model for predictive analytics
new_data = pd.DataFrame({'feature1': [1.2], 'feature2': [3.4], 'feature3': [5.6]})
prediction = model.predict(new_data)
print('Prediction:', prediction)
