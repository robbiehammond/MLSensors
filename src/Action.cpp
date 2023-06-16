#include "Action.h"

Action::Action(std::queue<SensorSample>& capturedSamples) {
    for (int i = 0; i < SAMPLES_PER_ACTION; i++) {
        lastSamples[i] = capturedSamples.front();
        capturedSamples.pop();
    }
}

/*
    Loop through accelData, see if there's a a quick jump 
    in the downwards acceleration (finger abruptly stopped)
*/
bool Action::likelyContainsButtonPress() {
    //start as first sample taken for this action
    //SensorSample prevSample = lastSamples[0];

    //Compare sample[i] to sample[i - 1]. The y acceleration for some sensor is beyond some threshold, this way probably a keypress.
    //Worth passing to the ML algorithm.
    for (int sample = 1; sample < SAMPLES_PER_ACTION; sample++) {
        SensorSample& curSample = lastSamples[sample];

        for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
            //int16_t prevYAcc = prevSample.get(sensorNum).ay;
            int16_t curYAcc = curSample.get(sensorNum).ay;
            if (curYAcc >= -1 * threshold) {
                return true;
            }
        }
    }
    return false;
}

void Action::writeOut(WriteOption w) {
    switch (w) {
        case SERIAL_OUT:
            std::for_each(std::begin(lastSamples), std::end(lastSamples), [](SensorSample& sample){
                Serial.println(sample.to_string().c_str());
            });
            //print data in a readable AND parsable format
            break;
        case BLUETOOTH:
            //send data via bluetooth 
            break;
        default:
            Serial.println("Unknown Write Option Used");
            break;
    }

}