import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras import Input, Model
import numpy as np
import itertools

SAMPLES_PER_ACTION = 6
NUM_SENSORS = 2 #(num chars / 6)

output_options = ['Right Hand', 'Left Hand']

def get_train_data():
    res = []
    f = open('src/ml/train_data.txt')
    lines = f.readlines()
    tmp = []
    for line in lines:
        sensorRead = line.split()
        for i in range(len(sensorRead)):
            sensorRead[i] = int(sensorRead[i])
        tmp.append(sensorRead)
        if (len(tmp) == SAMPLES_PER_ACTION):
            res.append(tmp)
            tmp.clear()
    return res

def get_train_labels():
    res = []
    f = open('src/ml/train_labels.txt')
    lines = f.readlines()
    for line in lines:
        res.append(int(line[0]))
    return res


train_data = get_train_data()
train_labels = get_train_labels()

if (len(train_data) != len(train_labels)): 
    print("train data and train labels diff sizes. Something went wrong.")




model = tf.keras.models.Sequential([
    Dense(6 * SAMPLES_PER_ACTION * NUM_SENSORS, activation=tf.nn.relu),
    tf.keras.layers.Dropout(0.1),
    Dense(NUM_SENSORS),
])


print(train_data)
print(len(train_data))
print(train_labels)
print(len(train_labels))

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


#model.fit(train_data, train_labels, epochs=10)