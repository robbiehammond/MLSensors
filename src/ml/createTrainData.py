import json, serial, csv, random, os, warnings
from termcolor import colored
from constants import * 
warnings.simplefilter('always', UserWarning)


def getTrainingDataLineByLine(ser, text):
    strokes_made = 0
    while (strokes_made < len(text)):
        key = text[strokes_made]
        print("Do the action corresponding to this character: " + key)
        line = ser.readline()
        try:
            data = json.loads(line)
            data['key'] = key
            write_entry_to_csv(data)
            print('Actions Performed: ' + str(strokes_made))
            strokes_made += 1
        except json.JSONDecodeError:
            ser.close()
            _ = input("Hardware is throwing errors. Press any key when ready to continue")
            ser.open()
        except UnicodeDecodeError:
            ser.close()
            _ = input("Hardware reset detected. Press any key when ready to continue")
            ser.open()
        print()

def write_entry_to_csv(obj):
    with open('src/ml/csvs/mpu6050data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        rowToWrite = []
        goodData = True
        for sampleNum in range(NUM_SAMPLES):
            for sensorNum in range(NUM_SENSORS):
                ax = obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['ax']
                ay = obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['ay']
                az = obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['az']
                gx = obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['gx']
                gy = obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['gy']
                gz = obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['gz']
                #if the sensor is likely not reading, give a warning
                if ax == 0 and ay == 0 and az == 0 and gx == 0 and gy == 0 and gz == 0:
                    goodData = False
                else:
                    rowToWrite.append(ax)
                    rowToWrite.append(ay)
                    rowToWrite.append(az)
                    rowToWrite.append(gx)
                    rowToWrite.append(gy)
                    rowToWrite.append(gz)


        if goodData:
            rowToWrite.append(obj['key'])
            writer.writerow(rowToWrite)
        else:
            warnings.warn(colored(f'Sensor {sensorNum} likely isn\'t responding. Data won\'t be recorded', 'red'))


def write_columns_to_csv():
    with open('src/ml/csvs/mpu6050data.csv', 'w+', newline='') as csvfile:
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


def main():
    # write columns if empty
    if os.stat('src/ml/csvs/mpu6050data.csv').st_size == 0:
        write_columns_to_csv() 
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
    getTrainingDataLineByLine(ser, text)


if __name__ == '__main__':
    main()