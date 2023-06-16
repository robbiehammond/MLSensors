#include "Action.h"

Action::Action(std::array<AccelData, SAMPLES_PER_ACTION> lastSamples) {
    this->lastSamples = lastSamples;
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