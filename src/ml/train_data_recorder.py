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
    print(data)
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
        'sample0s0ax', 'sample0s0ay', 'sample0s0az', 'sample0s0gx', 'sample0s0gy', 'sample0s0gz', 
        'sample1s0ax', 'sample1s0ay', 'sample1s0az', 'sample1s0gx', 'sample1s0gy', 'sample1s0gz', 
        'sample2s0ax', 'sample2s0ay', 'sample2s0az', 'sample2s0gx', 'sample2s0gy', 'sample2s0gz', 
        'sample3s0ax', 'sample3s0ay', 'sample3s0az', 'sample3s0gx', 'sample3s0gy', 'sample3s0gz', 
        'sample4s0ax', 'sample4s0ay', 'sample4s0az', 'sample4s0gx', 'sample4s0gy', 'sample4s0gz', 
        'sample5s0ax', 'sample5s0ay', 'sample5s0az', 'sample5s0gx', 'sample5s0gy', 'sample5s0gz', 
        'sample6s0ax', 'sample6s0ay', 'sample6s0az', 'sample6s0gx', 'sample6s0gy', 'sample6s0gz', 
        'sample7s0ax', 'sample7s0ay', 'sample7s0az', 'sample7s0gx', 'sample7s0gy', 'sample7s0gz', 
        'sample8s0ax', 'sample8s0ay', 'sample8s0az', 'sample8s0gx', 'sample8s0gy', 'sample8s0gz', 
        'sample9s0ax', 'sample9s0ay', 'sample9s0az', 'sample9s0gx', 'sample9s0gy', 'sample9s0gz',
        'key'
    ]
    writer.writerow(fields)
    cnt = 0
    for obj in jsonObjs:
        r = 1
        if cnt > 50:
            r = 2
        writer.writerow([
            obj['sample0']['s0']['ax'], obj['sample0']['s0']['ay'], obj['sample0']['s0']['az'], obj['sample0']['s0']['gx'], obj['sample0']['s0']['gy'], obj['sample0']['s0']['gz'],
            obj['sample1']['s0']['ax'], obj['sample1']['s0']['ay'], obj['sample1']['s0']['az'], obj['sample1']['s0']['gx'], obj['sample1']['s0']['gy'], obj['sample1']['s0']['gz'], 
            obj['sample2']['s0']['ax'], obj['sample2']['s0']['ay'], obj['sample2']['s0']['az'], obj['sample2']['s0']['gx'], obj['sample2']['s0']['gy'], obj['sample2']['s0']['gz'],
            obj['sample3']['s0']['ax'], obj['sample3']['s0']['ay'], obj['sample3']['s0']['az'], obj['sample3']['s0']['gx'], obj['sample3']['s0']['gy'], obj['sample3']['s0']['gz'], 
            obj['sample4']['s0']['ax'], obj['sample4']['s0']['ay'], obj['sample4']['s0']['az'], obj['sample4']['s0']['gx'], obj['sample4']['s0']['gy'], obj['sample4']['s0']['gz'],
            obj['sample5']['s0']['ax'], obj['sample5']['s0']['ay'], obj['sample5']['s0']['az'], obj['sample5']['s0']['gx'], obj['sample5']['s0']['gy'], obj['sample5']['s0']['gz'], 
            obj['sample6']['s0']['ax'], obj['sample6']['s0']['ay'], obj['sample6']['s0']['az'], obj['sample6']['s0']['gx'], obj['sample6']['s0']['gy'], obj['sample6']['s0']['gz'], 
            obj['sample7']['s0']['ax'], obj['sample7']['s0']['ay'], obj['sample7']['s0']['az'], obj['sample7']['s0']['gx'], obj['sample7']['s0']['gy'], obj['sample7']['s0']['gz'], 
            obj['sample8']['s0']['ax'], obj['sample8']['s0']['ay'], obj['sample8']['s0']['az'], obj['sample8']['s0']['gx'], obj['sample8']['s0']['gy'], obj['sample8']['s0']['gz'], 
            obj['sample9']['s0']['ax'], obj['sample9']['s0']['ay'], obj['sample9']['s0']['az'], obj['sample9']['s0']['gx'], obj['sample9']['s0']['gy'], obj['sample9']['s0']['gz'], 
            r
        ])
        cnt += 1