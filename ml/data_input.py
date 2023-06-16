'''
    Data input could be a 10-tuple (dataAcc1, dataAcc2, ..., dataAccN).
    Each piece of data could be of the form [maxAccelInLastXFrames, gyro data]
    Data is captured every time a keypress is made 


    Data Path:
        For training: Get data from ESP (just print to serial), write to file, train.
        For Use: Get data from ESP via bluetooth, feed to NN, use pynput to caues keypress
'''

import serial 

ser = serial.Serial('COM4', 9800, timeout=1)
print(serial.__version__)
while (True):
    line = ser.readline()
    print(line.decode().strip())
time.sleep(3)
keyboard.press('a')


'''
from pynput.keyboard import Key, Listener

def on_press(key):
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
'''
