import json, serial, csv, random

ser = serial.Serial('/dev/tty.usbserial-02896C6F')
ser.baudrate = 922190

jsonObjs = []

cnt = 0
while (True):
    print(cnt)
    if cnt % 50 == 0:
        print("CHANGE!")
    line = ser.readline()
    # We might start reading halfway through an object, just wait a bit to skip those.
    data = json.loads(line)
    jsonObjs.append(data)
    print(data)
    cnt += 1
    if cnt >= 200:
        break

with open('src/ml/csvs/mpu6050data.csv', 'w', newline='') as csvfile:
    #change these when more sensors are in use
    NUM_SENSORS = 2
    NUM_SAMPLES = 10
    writer = csv.writer(csvfile)

    fields = []
    # append sample0s0ax, sample0s0ay, ... sampleNsMgz
    for sampleNum in range(10):
        for sensorNum in range(2):
            fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'ax\'')
            fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'ay\'')
            fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'az\'')
            fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gx\'')
            fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gy\'')
            fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gz\'')
    fields.append('key')

    writer.writerow(fields)
    cnt = 0
    for obj in jsonObjs:
        r = (cnt // 50) + 1

        rowToWrite = []
        for sampleNum in range(10):
            for sensorNum in range(2):
                rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['ax'])
                rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['ay'])
                rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['az'])
                rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['gx'])
                rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['gy'])
                rowToWrite.append(obj['sample' + str(sampleNum)]['s' + str(sensorNum)]['gz'])
        rowToWrite.append(r)
        
        writer.writerow(rowToWrite)
        cnt += 1