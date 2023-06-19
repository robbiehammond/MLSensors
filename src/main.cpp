#include <MPU6050.h>
#include <queue>
#include "Action.h"
bool TEST = false; //to check sensor sampling rate

MPU6050 sensor; //sensor that is currently being looked at
int16_t rawVals[6]; //where raw data is read to
SensorState curState; //written to over and over again for a copy to get pushed into samples.
std::array<SensorState, MAX_RECORDED_SAMPLES> capturedStates; //After button press, the last few states are sent over. The last 1000 are stored here.
Action curAction; //When a button press happens, it's stored here.
int sampleInd = 0; //loops through capturedSamples updating them every loop
bool enoughSamplesCollected = false; //turns true when we have 10 samples collected 
int maxAy = 0; //for threshold tuning

//TODO: Move these to constants.h
const static int SENSOR0PIN = A0;
const static int SENSOR1PIN = A1;
const static int SENSOR2PIN = GPIO_NUM_13;
const static int SENSOR3PIN = GPIO_NUM_12;

//Sensor reads will come from the input sensor number.
//HIGH = address is now 0x69, low means it's 0x68.
//Device we want will be on 0x68.
void changeSensor(int sensor) {
    switch (sensor) {
        case 0:
            digitalWrite(SENSOR0PIN, LOW);
            digitalWrite(SENSOR1PIN, HIGH);
            digitalWrite(SENSOR2PIN, HIGH);
            digitalWrite(SENSOR3PIN, HIGH);
            break;
        case 1:
            digitalWrite(SENSOR0PIN, HIGH);
            digitalWrite(SENSOR1PIN, LOW);
            digitalWrite(SENSOR2PIN, HIGH);
            digitalWrite(SENSOR3PIN, HIGH);
            break;
        case 2:
            digitalWrite(SENSOR0PIN, HIGH);
            digitalWrite(SENSOR1PIN, HIGH);
            digitalWrite(SENSOR2PIN, LOW);
            digitalWrite(SENSOR3PIN, HIGH);
            break;
        case 3:
            digitalWrite(SENSOR0PIN, HIGH);
            digitalWrite(SENSOR1PIN, HIGH);
            digitalWrite(SENSOR2PIN, HIGH);
            digitalWrite(SENSOR3PIN, LOW);
            break;
        default:
            Serial.println("Invalid pin passed.");
            Serial.println(sensor);
    }
}

//read current sensor data, compile it into the SensorSample. After this is called, the curSample has the most up-to-date data.
void updateSensorData() {
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
        changeSensor(sensorNum); //change to right sensor

        sensor.getMotion6(&rawVals[iAx], &rawVals[iAy], &rawVals[iAz], 
                          &rawVals[iGx], &rawVals[iGy], &rawVals[iGz]);

        if (rawVals[iAy] > maxAy) { 
            maxAy = rawVals[iAy];
        }

        curState.set(sensorNum, rawVals);
    };
}

//Give it it's timestamp of when it was taken, and put it into the capturedSamples list.
void recordSensorData() {
    curState.markAsCompleted();
    capturedStates[sampleInd] = curState;
    curState.resetState();
}


/*
Loop through all the sensors and check their most recently recorded y acceleration. If it abruptly changes 
in whatever direction is up, it was probably a keypress.

Probably could just be done immediately in updateSensorData() so we don't need to loop over everything again. Eh it's probably fine.
*/
bool possiblePress() {
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
        int16_t curXAcc = curState.get(sensorNum).ax;
        int16_t curYAcc = curState.get(sensorNum).ay;
        int16_t curZAcc = curState.get(sensorNum).az;
        // not just y! You can tilt the device and stuff too!
        if (curXAcc >= THRESHOLD || curYAcc >= THRESHOLD || curZAcc >= THRESHOLD) {
            return true;
        }

    }
    return false;
}


void setup() {

    Serial.begin(922190);
    pinMode(SENSOR0PIN, OUTPUT);
    Wire.begin();

    sensor = MPU6050(0x68);

    sensor.initialize();
    for (int i = 0; i < NUM_SENSORS; i++) {
        changeSensor(i);
        Serial.println(sensor.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));
        sensor.setFullScaleAccelRange(MPU6050_ACCEL_FS_16);
    }

}

/*
For 1 sensor, normally executes in 1-2 ms (between 500 Hz and 1 kHz), but when it's time to print,
it takes around 16-17 ms.

For 4 sensors, normally executes in 6-7 ms, but when it's time to print,
it takes about 50-52 ms.
*/
void loop() {
    //long int t1 = millis();
    if (!enoughSamplesCollected && sampleInd > 10) enoughSamplesCollected = true;

    updateSensorData();

    recordSensorData();

    if (enoughSamplesCollected && possiblePress()) {

        std::array<SensorState, SAMPLES_PER_ACTION> statesToUse;
        for (int i = 0; i < SAMPLES_PER_ACTION; i++) {
            //if index is low but samples at the end of the array are good, use those.
            int loopingSampleInd = sampleInd - i < 0 ? MAX_RECORDED_SAMPLES - i : sampleInd;
            //just so that samplesToUse[0] is oldest, samplesToUse[1] is next oldest, etc
            statesToUse[SAMPLES_PER_ACTION - 1 - i] = capturedStates[loopingSampleInd - i];
        }

        curAction.setStates(statesToUse);
        curAction.writeOut(WriteOption::SERIAL_OUT);
    }
    sampleInd = (sampleInd + 1) % MAX_RECORDED_SAMPLES;
    //Serial.println(millis() - t1);
}