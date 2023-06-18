#include <MPU6050.h>
#include <queue>
#include "Action.h"

/*
    Instead of queuing readings up, we could simply 
    store like 10000 of them and check for a potential 
    button press on each iteration by checking the 
    current (and possibly past 1 or 2) ay. 
    If it looks like it was a button press, give the 
    last X samples for learning.
*/

int16_t rawVals[6]; //where raw data is read to
std::array<MPU6050, NUM_SENSORS> sensors;
SensorSample curSample; //written to over and over again for a copy to get pushed into samples.
std::array<SensorSample, MAX_RECORDED_SAMPLES> capturedSamples;
int sampleInd = 0;


//read current sensor data, compile it into the SensorSample. After this is called, the curSample has the most up-to-date data.
void updateSensorData() {
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
        auto& sensor = sensors[sensorNum];
        long int t1 = millis();
        sensor.getMotion6(&rawVals[iAx], &rawVals[iAy], &rawVals[iAz], 
                          &rawVals[iGx], &rawVals[iGy], &rawVals[iGz]);
        Serial.println(millis() - t1);

        curSample.set(sensorNum, rawVals);
    };
}

//Give it it's timestamp of when it was taken, and put it into the capturedSamples list.
void recordSensorData() {
    curSample.finalizeSample();
    capturedSamples[sampleInd] = curSample;
    curSample.resetSample();
}


/*
Loop through all the sensors and check their most recently recorded y acceleration. If it abruptly changes 
in whatever direction is up, it was probably a keypress.

Probably could just be done immediately in updateSensorData() so we don't need to loop over everything again. Eh it's probably fine.
*/
bool possiblePress() {
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
        int16_t curYAcc = curSample.get(sensorNum).ay;
        if (curYAcc >= -1 * THRESHOLD) {
            return true;
        }
    }
    return false;
}

void setup() {
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    Serial.begin(9600);

    for (auto& sensor : sensors) {
        sensor.initialize();
    }
}



void loop() {
    updateSensorData();

    recordSensorData();

    if (possiblePress()) {

        //TODO: This is a bug to fix: If sampleInd is at the beginning and we have an action, it won't be registered.
        //This is because we just look backwards in the sample list to get the last few samples.
        if (sampleInd >= SAMPLES_PER_ACTION) {
            std::array<SensorSample, SAMPLES_PER_ACTION> samplesToUse;
            for (int i = 0; i < SAMPLES_PER_ACTION; i++) {
                //just so that samplesToUse[0] is oldest, samplesToUse[1] is next oldest, etc
                samplesToUse[SAMPLES_PER_ACTION - 1 - i] = capturedSamples[sampleInd - i];
            }

            Action action(samplesToUse);
            action.writeOut(WriteOption::SERIAL_OUT);

        }
    }
    sampleInd = (sampleInd + 1) % MAX_RECORDED_SAMPLES;
}