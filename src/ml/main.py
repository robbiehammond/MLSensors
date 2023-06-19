from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
import pandas as pd 
from keras.models import load_model
import serial, json
import numpy as np
from constants import * 

def predict(model, data):
    nnInput = []
    for sampleNum in range(NUM_SAMPLES):
        for sensorNum in range(NUM_SENSORS):
            nnInput.append(data['sample' + str(sampleNum)]['s' + str(sensorNum)]['ax'])
            nnInput.append(data['sample' + str(sampleNum)]['s' + str(sensorNum)]['ay'])
            nnInput.append(data['sample' + str(sampleNum)]['s' + str(sensorNum)]['az'])
            nnInput.append(data['sample' + str(sampleNum)]['s' + str(sensorNum)]['gx'])
            nnInput.append(data['sample' + str(sampleNum)]['s' + str(sensorNum)]['gy'])
            nnInput.append(data['sample' + str(sampleNum)]['s' + str(sensorNum)]['gz'])
    df = pd.DataFrame(data=[nnInput], columns=fields)
    t = scaler.transform(df)
    print(np.argmax(model.predict(t)))

def main():
    model = load_model('src/ml/models/model.h5')
    ser = serial.Serial(DEVICE_LOCATION)
    ser.baudrate = BAUD_RATE
    while (True):
        line = ser.readline()
        data = json.loads(line)
        predict(model, data)

if __name__ == '__main__':
    main()
