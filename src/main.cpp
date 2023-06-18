#include <MPU6050.h>
#include <queue>
#include "Action.h"
bool TEST = false; //to check sensor sampling rate

int16_t rawVals[6]; //where raw data is read to
std::array<MPU6050, NUM_SENSORS> sensors;
SensorState curState; //written to over and over again for a copy to get pushed into samples.
std::array<SensorState, MAX_RECORDED_SAMPLES> capturedStates;
Action curAction;
int sampleInd = 0;
bool enoughSamplesCollected = false; //turns true when we have 10 samples collected 
int maxAy = 0;


//read current sensor data, compile it into the SensorSample. After this is called, the curSample has the most up-to-date data.
void updateSensorData() {
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
        auto& sensor = sensors[sensorNum];

        sensor.getMotion6(&rawVals[iAx], &rawVals[iAy], &rawVals[iAz], 
                          &rawVals[iGx], &rawVals[iGy], &rawVals[iGz]);
        if (rawVals[iAy] > maxAy) { 
            maxAy = rawVals[iAy];
            Serial.println(maxAy);
        }
        curState.set(sensorNum, rawVals);
    };
}

//Give it it's timestamp of when it was taken, and put it into the capturedSamples list.
void recordSensorData() {
    curState.markAsCompleted();
    capturedStates[sampleInd] = curState;
    curState.resetState();
    sampleInd = (sampleInd + 1) % MAX_RECORDED_SAMPLES;
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

void checkSampleRate() {
    long int t1 = millis();
    sensors[0].getMotion6(&rawVals[iAx], &rawVals[iAy], &rawVals[iAz], 
                        &rawVals[iGx], &rawVals[iGy], &rawVals[iGz]);
    Serial.println(millis() - t1);
}

void setup() {
    Serial.begin(922190);
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    for (auto& sensor : sensors) {
        sensor.initialize();
        Serial.println(sensor.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));
        sensor.setFullScaleAccelRange(MPU6050_ACCEL_FS_16);

    }
}


void loop() {
    if (sampleInd > 10) enoughSamplesCollected = true;

    if (TEST) {
        checkSampleRate();
        return;
    }


    updateSensorData();

    recordSensorData();

    if (enoughSamplesCollected && possiblePress()) {

        std::array<SensorState, SAMPLES_PER_ACTION> statesToUse;
        for (int i = 0; i < SAMPLES_PER_ACTION; i++) {
            int loopingSampleInd = sampleInd - i < 0 ? MAX_RECORDED_SAMPLES - i : sampleInd;
            //just so that samplesToUse[0] is oldest, samplesToUse[1] is next oldest, etc
            statesToUse[SAMPLES_PER_ACTION - 1 - i] = capturedStates[loopingSampleInd - i];
        }
        curAction.setStates(statesToUse);
        curAction.writeOut(WriteOption::SERIAL_OUT);
    }
}