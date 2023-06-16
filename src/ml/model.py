import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras import Input
import numpy as np
import itertools

def data_generator():
    while(True):
        number1 = np.random.uniform();
        number2 = np.random.uniform();
        # our input data is an array containing 2 numbers
        X = [number1, number2]
        # our label is 1 or 0
        Y = 1 if number2 > number1 else 0
        # our generator should return the input data and the label
        yield X, [Y]
        
# create a dataset from our generator
train_dataset = tf.data.Dataset.from_generator(
    data_generator, 
    output_types = (tf.float32, tf.int32),
    output_shapes=((2), (1))
)
train_dataset = train_dataset.batch(batch_size=30)

model = Sequential([
    Input(shape=(2)),
    Dense(5, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics=['accuracy'])

print(model.summary())

model.fit(
    train_dataset,
    steps_per_epoch=1000,
    epochs=5
)
