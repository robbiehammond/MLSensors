#include "Action.h"

Action::Action(std::array<SensorSample, SAMPLES_PER_ACTION>& capturedSamples) {
    lastSamples = capturedSamples;
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