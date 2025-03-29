import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.regularizers import l2
from kerastuner import HyperModel, RandomSearch
import matplotlib.pyplot as plt
import tensorflow as tf

# Load the dataset
df = pd.read_csv('dataset.csv')

# Preprocess the data
X = df.drop(['target'], axis=1)
y = df['target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define the model architecture
class MyHyperModel(HyperModel):
    def build(self, hp):
        model = Sequential()
        model.add(Dense(hp.Int('units_1', min_value=128, max_value=512, step=64), activation='relu', input_shape=(X_train.shape[1],), kernel_regularizer=l2(0.01)))
        model.add(BatchNormalization())
        model.add(Dropout(0.3))
        model.add(Dense(hp.Int('units_2', min_value=128, max_value=512, step=64), activation='relu', kernel_regularizer=l2(0.01)))
        model.add(BatchNormalization())
        model.add(Dropout(0.3))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(optimizer=tf.keras.optimizers.Adam(hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
        return model

# Hyperparameter tuning
tuner = RandomSearch(MyHyperModel(),
                     objective='val_accuracy',
                     max_trials=10,
                     executions_per_trial=1,
                     directory='my_dir',
                     project_name='helloworld')

tuner.search(X_train, y_train, epochs=100, validation_split=0.2)

# Get the best model
best_model = tuner.get_best_models(num_models=1)[0]

# Callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1)
model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True, verbose=1)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=1e-6, verbose=1)

# Train the model
history = best_model.fit(X_train, y_train, validation_split=0.2, epochs=100, batch_size=32, 
                          callbacks=[early_stopping, model_checkpoint, reduce_lr])

# Plot the training history
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# Load the best model
best_model.load_weights('best_model.h5')

# Make predictions on the test set
y_pred = best_model.predict(X_test)
y_pred = np.round(y_pred)

# Evaluate the model
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
accuracy = accuracy_score(y_test, y_pred)
confusion_matrix_result = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

print('Accuracy:', accuracy)
print('Confusion matrix:')
print(confusion_matrix_result)
print('Classification report:')
print(report)
