import json, serial, csv, random
from constants import * 

def getTrainingData(ser, num_keystrokes):
    print("Type \'quit\' to save data.")
    jsonObjs = []
    strokes_made = 0
    while (strokes_made < num_keystrokes):
        print("Do an action.")
        line = ser.readline()
        strokes_made += 1

        key = input("Action recorded! Press the key on the keyboard that this should correspond to, then press enter: ")
        if (key == 'quit'):
            break
        print(key)
        data = json.loads(line)
        data['key'] = key
        jsonObjs.append(data)

        print('Actions Performed: ' + str(strokes_made))
        print()
    return jsonObjs


def write_to_csv(jsonObjs):
    with open('src/ml/csvs/mpu6050data.csv', 'w', newline='') as csvfile:
        #change these when more sensors are in use
        NUM_SENSORS = 2
        NUM_SAMPLES = 10
        writer = csv.writer(csvfile)

        fields = []
        # append sample0s0ax, sample0s0ay, ... sampleNsMgz
        for sampleNum in range(NUM_SAMPLES):
            for sensorNum in range(NUM_SENSORS):
                fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'ax\'')
                fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'ay\'')
                fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'az\'')
                fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gx\'')
                fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gy\'')
                fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gz\'')
        fields.append('key')

        writer.writerow(fields)
        for obj in jsonObjs:
            rowToWrite = []
            for sampleNum in range(NUM_SAMPLES):
                for sensorNum in range(NUM_SENSORS):
                    rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['ax'])
                    rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['ay'])
                    rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['az'])
                    rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['gx'])
                    rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['gy'])
                    rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['gz'])
            rowToWrite.append(obj['key'])
            writer.writerow(rowToWrite)
            


def main():
    ser = serial.Serial(DEVICE_LOCATION)
    ser.baudrate = BAUD_RATE
    objs = getTrainingData(ser, NUM_KEYSTROKES_TO_TRAIN)
    write_to_csv(objs)



if __name__ == '__main__':
    main()