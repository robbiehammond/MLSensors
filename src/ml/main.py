from keras.models import load_model
import serial, json
import numpy as np
from sklearn.calibration import LabelEncoder
from constants import * 
from pynput.keyboard import Key, Controller

keyboard = Controller()
encoder = LabelEncoder()
encoder.fit(y_train)

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

    guess = model.predict(t)
    keyToPress = encoder.inverse_transform([np.argmax(guess)])[0]
    if ONLYPRINT:
        print(keyToPress)
    else:
        key = None
        if keyToPress == 'Key.space':
            key = Key.space
            keyboard.press(key)
        elif keyToPress == 'Key.shift':
            key = Key.shift
            keyboard.press(key)
        else:
            key = keyToPress
            keyboard.press(str(key))

def main():
    model = load_model('src/ml/models/model.h5')
    ser = serial.Serial(DEVICE_LOCATION)
    ser.baudrate = BAUD_RATE
    print("Ready to recieve input.")
    while (True):
        line = ser.readline()
        try:
            data = json.loads(line)
            predict(model, data)
        except json.JSONDecodeError:
            ser.close()
            _ = input("Hardware is throwing errors. Press any key when ready to continue")
            ser.open()
        except UnicodeDecodeError:
            ser.close()
            _ = input("Hardware reset detected. Press any key when ready to continue")
            ser.open()

if __name__ == '__main__':
    main()