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
    print(ar)
    right = 0
    print(type(y_test))
    for i in range(len(y_test)):
        print("Predicted " + str(CONTROL_SCHEME[(np.argmax(predictions[i]))]), end=', ')
        print("Actually was " + str(ar[i]))
        if (str(CONTROL_SCHEME[(np.argmax(predictions[i]))]) == str(ar[i])):
            right += 1
    print("Test set accuracy: " + str(right / len(predictions)))



tf.random.set_seed(2)


encoder = LabelEncoder()
encoder.fit(y_train)
encoded_Y = encoder.transform(y_train)
dummy_y = tf.keras.utils.to_categorical(encoded_Y)
dummy_y_test = tf.keras.utils.to_categorical(encoder.transform(y_test))

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


model = tf.keras.Sequential([
    tf.keras.layers.Dense(NUM_SAMPLES * 6 * NUM_SENSORS, activation='gelu'),
    tf.keras.layers.Dense(1024, activation='gelu'),
    tf.keras.layers.Dense(512, activation='gelu'),
    tf.keras.layers.Dense(NUM_POSSIBILITIES, activation='sigmoid')
])

#Optimizers tried that seem somewhat promising: adadelta, 
model.compile(
    loss='categorical_crossentropy',
    optimizer='adadelta',
    metrics=[
        'accuracy'
    ]
)

history = model.fit(X_train_scaled, dummy_y, epochs=300, validation_data=(X_test_scaled, dummy_y_test))
predictions_raw = model.predict(X_test_scaled)
predictions = []
for pred in predictions_raw:
    predictions.append(np.argmax(pred))

print(y_test)
print(encoder.inverse_transform(predictions))


model.save('src/ml/models/model.h5')
