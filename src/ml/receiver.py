import json, serial

ser = serial.Serial('/dev/tty.usbserial-02896C6F')
ser.baudrate = 922190

cnt = 1
while (True):
    line = ser.readline()
    if (cnt > 10):
        data = json.loads(line)
        print(data['sample0'])
    cnt += 1
