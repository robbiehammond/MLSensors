import serial
ser = serial.Serial('COM4', 9800, timeout=1)
print(serial.__version__)
while (True):
    line = ser.readline()
    print(line.decode().strip())