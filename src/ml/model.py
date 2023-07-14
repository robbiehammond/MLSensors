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


# Through trial and error, Adadelta seems to work well, but there might be better ones out there.
model.compile(
    loss='categorical_crossentropy',
    optimizer='adadelta',
    metrics=[
        'accuracy'
    ]
)

history = model.fit(X_train_scaled, dummy_y, epochs=NUM_EPOCHS, validation_data=(X_test_scaled, dummy_y_test))

filename = input("Training Finished. Enter a name for the .h5 file (not including the .h5 extension). If left blank, the name will be \'model\'.")

if filename == "":
    model.save('src/ml/models/model.h5')
else:
    model.save(f'src/ml/models/{filename}.h5')

print("Saved.")
    