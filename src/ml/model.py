from sklearn.calibration import LabelEncoder
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras import Input, Model
import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from constants import * 




def printTestResults(y_test, predictions):
    ar = [d for d in y_test]
    right = 0
    print(type(y_test))
    for i in range(len(y_test)):
        print("Predicted " + str(np.argmax(predictions[i]) + 1), end=', ')
        print("Actually was " + str(ar[i]))
        if (str(np.argmax(predictions[i]) + 1) == str(ar[i])):
            right += 1
    print("Test set accuracy: " + str(right / len(predictions)))



tf.random.set_seed(2)


encoder = LabelEncoder()
encoder.fit(y_train)
encoded_Y = encoder.transform(y_train)
dummy_y = tf.keras.utils.to_categorical(encoded_Y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(NUM_POSSIBILITIES, activation='sigmoid')
])
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=[
        'accuracy'
    ]
)

history = model.fit(X_train_scaled, dummy_y, epochs=100)
predictions = model.predict(X_test_scaled)

printTestResults(y_test, predictions)

model.save('src/ml/models/model.h5')
