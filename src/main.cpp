#include <MPU6050.h>
#include <queue>
#include "Action.h"

int16_t rawVals[6]; //where raw data is read to
std::array<MPU6050, NUM_SENSORS> sensors; //sensors[0] = LH pinky, sensors[1] = LH ring, etc
SensorSample curSample; //written to over and over again for a copy to get pushed into samples.
std::queue<SensorSample> capturedSamples; //queue containing the last SAMPLES_PER_ACTION samples.


//read current sensor data, compile it into a SensorSample
void updateSensorData() {
    int sensorNum = 0;
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
        auto& sensor = sensors[sensorNum];
        sensor.getMotion6(&rawVals[iAx], &rawVals[iAy], &rawVals[iAz], 
                          &rawVals[iGx], &rawVals[iGy], &rawVals[iGz]);
        curSample.set(sensorNum, rawVals);
        
        sensorNum++;
    };
}

//write out timestamp and push it into queue
void recordSensorData() {
    curSample.finalizeSample();
    capturedSamples.push(curSample);
    curSample.resetSample();
}

void setup() {
}


void loop() {
    updateSensorData();

    recordSensorData();

    if (capturedSamples.size() == SAMPLES_PER_ACTION) {

        //NOTE: This clears the capturedSamples queue too.
        Action action(capturedSamples);

        if (action.likelyContainsButtonPress())
            action.writeOut(WriteOption::SERIAL_OUT);
    }
}