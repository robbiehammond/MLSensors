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