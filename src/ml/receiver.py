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
import json, serial

ser = serial.Serial('/dev/tty.usbserial-02896C6F')
ser.baudrate = 922190

cnt = 0
while (True):
    line = ser.readline()
    # We might start reading halfway through an object, just wait a bit to skip those.
    if (cnt > 10):
        data = json.loads(line)
        print(data['sample0'])
    cnt += 1
