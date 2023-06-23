import json, serial, csv, random
from constants import * 


def getTrainingData(ser, text):
    jsonObjs = []
    strokes_made = 0
    i = 0
    while (i < len(text)):
        key = text[strokes_made]
        print("Do the action corresponding to this character: " + key)
        line = ser.readline()
        strokes_made += 1

        data = json.loads(line)
        data['key'] = key
        jsonObjs.append(data)

        print('Actions Performed: ' + str(strokes_made))
        print()
        if (strokes_made > 0) and (strokes_made % 50 == 0):
            ser.close()
            inp = input("Press any key when ready to continue")
            ser.open()
    return jsonObjs


def write_to_csv(jsonObjs):
    with open('src/ml/csvs/mpu6050data.csv', 'w', newline='') as csvfile:
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
    text = []
    with open('src/ml/train_data/train_inputs_no_keys.txt', 'r') as file:
        while True:
            c = file.read(1)
            if not c:
                break
            if c != '\n':
                text.append(c)

    objs = getTrainingData(ser, text)
    write_to_csv(objs)


if __name__ == '__main__':
    main()