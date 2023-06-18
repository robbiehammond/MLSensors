'''
    Data format:
        {
            sample0:
            {
                time: XXXXX
                data: 
                {
                    sensor0:
                    {
                        ax: X
                        ay: X
                        az: X
                        gx: X
                        gy: X
                        gz: X
                    }
                }
            }
            sample1: ...
            sample2: ...
        }

    NN can have SAMPLES_PER_ACTION * NUM_SENSORS fields
'''
import json, serial, csv, random

ser = serial.Serial('/dev/tty.usbserial-02896C6F')
ser.baudrate = 922190

jsonObjs = []
cnt = 0
while (True):
    line = ser.readline()
    # We might start reading halfway through an object, just wait a bit to skip those.
    data = json.loads(line)
    jsonObjs.append(data)
    print(data['sample0'])
    cnt += 1
    if cnt == 50:
        print("CHANGE!")
    if cnt > 100:
        break

with open('src/ml/csvs/mpu6050data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # for 10 samples, 2 sensors at the moment. 12 pieces of data per sample, 10 samples
    # Some of the most cursed code I've ever written
    fields = [
        'sample0sensor0ax', 'sample0sensor0ay', 'sample0sensor0az', 'sample0sensor0gx', 'sample0sensor0gy', 'sample0sensor0gz', 
        'sample1sensor0ax', 'sample1sensor0ay', 'sample1sensor0az', 'sample1sensor0gx', 'sample1sensor0gy', 'sample1sensor0gz', 
        'sample2sensor0ax', 'sample2sensor0ay', 'sample2sensor0az', 'sample2sensor0gx', 'sample2sensor0gy', 'sample2sensor0gz', 
        'sample3sensor0ax', 'sample3sensor0ay', 'sample3sensor0az', 'sample3sensor0gx', 'sample3sensor0gy', 'sample3sensor0gz', 
        'sample4sensor0ax', 'sample4sensor0ay', 'sample4sensor0az', 'sample4sensor0gx', 'sample4sensor0gy', 'sample4sensor0gz', 
        'sample5sensor0ax', 'sample5sensor0ay', 'sample5sensor0az', 'sample5sensor0gx', 'sample5sensor0gy', 'sample5sensor0gz', 
        'sample6sensor0ax', 'sample6sensor0ay', 'sample6sensor0az', 'sample6sensor0gx', 'sample6sensor0gy', 'sample6sensor0gz', 
        'sample7sensor0ax', 'sample7sensor0ay', 'sample7sensor0az', 'sample7sensor0gx', 'sample7sensor0gy', 'sample7sensor0gz', 
        'sample8sensor0ax', 'sample8sensor0ay', 'sample8sensor0az', 'sample8sensor0gx', 'sample8sensor0gy', 'sample8sensor0gz', 
        'sample9sensor0ax', 'sample9sensor0ay', 'sample9sensor0az', 'sample9sensor0gx', 'sample9sensor0gy', 'sample9sensor0gz',
        'key'
    ]
    writer.writerow(fields)
    cnt = 0
    for obj in jsonObjs:
        r = 1
        if cnt > 50:
            r = 2
        writer.writerow([
            obj['sample0']['sensor0']['ax'], obj['sample0']['sensor0']['ay'], obj['sample0']['sensor0']['az'], obj['sample0']['sensor0']['gx'], obj['sample0']['sensor0']['gy'], obj['sample0']['sensor0']['gz'], 
            obj['sample1']['sensor0']['ax'], obj['sample1']['sensor0']['ay'], obj['sample1']['sensor0']['az'], obj['sample1']['sensor0']['gx'], obj['sample1']['sensor0']['gy'], obj['sample1']['sensor0']['gz'], 
            obj['sample2']['sensor0']['ax'], obj['sample2']['sensor0']['ay'], obj['sample2']['sensor0']['az'], obj['sample2']['sensor0']['gx'], obj['sample2']['sensor0']['gy'], obj['sample2']['sensor0']['gz'], 
            obj['sample3']['sensor0']['ax'], obj['sample3']['sensor0']['ay'], obj['sample3']['sensor0']['az'], obj['sample3']['sensor0']['gx'], obj['sample3']['sensor0']['gy'], obj['sample3']['sensor0']['gz'], 
            obj['sample4']['sensor0']['ax'], obj['sample4']['sensor0']['ay'], obj['sample4']['sensor0']['az'], obj['sample4']['sensor0']['gx'], obj['sample4']['sensor0']['gy'], obj['sample4']['sensor0']['gz'], 
            obj['sample5']['sensor0']['ax'], obj['sample5']['sensor0']['ay'], obj['sample5']['sensor0']['az'], obj['sample5']['sensor0']['gx'], obj['sample5']['sensor0']['gy'], obj['sample5']['sensor0']['gz'], 
            obj['sample6']['sensor0']['ax'], obj['sample6']['sensor0']['ay'], obj['sample6']['sensor0']['az'], obj['sample6']['sensor0']['gx'], obj['sample6']['sensor0']['gy'], obj['sample6']['sensor0']['gz'], 
            obj['sample7']['sensor0']['ax'], obj['sample7']['sensor0']['ay'], obj['sample7']['sensor0']['az'], obj['sample7']['sensor0']['gx'], obj['sample7']['sensor0']['gy'], obj['sample7']['sensor0']['gz'], 
            obj['sample8']['sensor0']['ax'], obj['sample8']['sensor0']['ay'], obj['sample8']['sensor0']['az'], obj['sample8']['sensor0']['gx'], obj['sample8']['sensor0']['gy'], obj['sample8']['sensor0']['gz'], 
            obj['sample9']['sensor0']['ax'], obj['sample9']['sensor0']['ay'], obj['sample9']['sensor0']['az'], obj['sample9']['sensor0']['gx'], obj['sample9']['sensor0']['gy'], obj['sample9']['sensor0']['gz'],
            r
        ])
        cnt += 1