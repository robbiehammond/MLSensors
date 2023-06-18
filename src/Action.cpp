#include "Action.h"

Action::Action(std::array<SensorState, SAMPLES_PER_ACTION>& capturedSamples) {
    lastSamples = capturedSamples;
}

void Action::writeOut(WriteOption w) {
    switch (w) {

        //print data in a readable AND parsable format
        case SERIAL_OUT: {
            //Create mega json object to hold all the samples
            JsonObject megaObject = buf.createNestedObject();

            //for each state, create jsonObject within big one.
            for (int sampleInd = 0; sampleInd < SAMPLES_PER_ACTION; sampleInd++) {
                auto& sample = lastSamples[sampleInd];
                megaObject["time"] = sample.getTimeStamp();

                //for each sensor, create json object within state object, add fields
                for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
                    std::string key = "sensor" + std::to_string(sensorNum);
                    JsonObject sensorData = megaObject.createNestedObject(key);
                    sensorData["ax"] = (int)sample.get(sensorNum).ax;
                    sensorData["ay"] = (int)sample.get(sensorNum).ay;
                    sensorData["az"] = (int)sample.get(sensorNum).az;
                    sensorData["gx"] = (int)sample.get(sensorNum).gx;
                    sensorData["gy"] = (int)sample.get(sensorNum).gy;
                    sensorData["gz"] = (int)sample.get(sensorNum).gz;
                }
            }
            serializeJson(megaObject, Serial);
            break;
        }

        case BLUETOOTH:
            //send data via bluetooth 
            break;

        default:
            Serial.println("Unknown Write Option Used");
            break;
    }

}