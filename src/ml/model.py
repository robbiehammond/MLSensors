import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras import Input, Model
import numpy as np
import itertools

SAMPLES_PER_ACTION = 6
NUM_SENSORS = 2 #(num chars / 6)
DATA_PER_SENSOR = 6

output_options = ['Right Hand', 'Left Hand']

def get_train_data():
    res = []
    f = open('src/ml/train_data.txt')
    lines = f.readlines()

    tmp = []
    for line in lines:

        if line == '\n':
            continue

        sensorRead = line.split()
        for i in range(len(sensorRead)):
            sensorRead[i] = int(sensorRead[i])

        tmp.append(sensorRead)

        if (len(tmp) == SAMPLES_PER_ACTION):
            res.append(tmp)
            tmp = []

    return np.array(res, dtype=int)


def get_train_labels():
    res = []
    f = open('src/ml/train_labels.txt')
    lines = f.readlines()
    for line in lines:
        res.append(int(line[0]))
    return np.array(res, dtype=int)


train_data = get_train_data()
print(train_data)
train_labels = get_train_labels()
print(train_labels)


if (len(train_data) != len(train_labels)): 
    print("train data and train labels diff sizes. Something went wrong.")
    exit()


model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    #Dense(10 * DATA_PER_SENSOR * SAMPLES_PER_ACTION * NUM_SENSORS, activation=tf.nn.relu),
    Dense(1, activation='sigmoid'),
])


model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

model.fit(train_data, train_labels, epochs=100)
t = tf.constant([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0]])

preds = model.predict(train_data)

print(preds)

print(model.summary())
