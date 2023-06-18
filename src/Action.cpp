#include "Action.h"

Action::Action() {
}

void Action::setStates(std::array<SensorState, SAMPLES_PER_ACTION>& capturedSamples) {
    lastSamples = capturedSamples;
}

// This will (theoretically) called on every button press action.
// It is somewhat slow to send the data out, meaning that 
// there will likely be some delay (like .25 sec) before data is collected again
// for the next press to be registered.
// The faster this can go, the faster you can rapid-fire press
void Action::writeOut(WriteOption w) {
    switch (w) {

        //print data in a readable AND parsable format
        case SERIAL_OUT: {
            DynamicJsonDocument doc(7500); //to format json and all that 

            //for each state, create jsonObject within big one.
            for (int sampleInd = 0; sampleInd < SAMPLES_PER_ACTION; sampleInd++) {
                //create json object for this sample
                std::string stateKey = "sample" + std::to_string(sampleInd);
                JsonObject sampleData = doc.createNestedObject(stateKey);

                auto& sample = lastSamples[sampleInd];
                int time = sample.getTimeStamp();

                sampleData["time"] = time;

                //for each sensor, create json object within timestamp , add fields
                for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
                    std::string key = "sensor" + std::to_string(sensorNum);
                    JsonObject sensorData = sampleData.createNestedObject(key);
                    sensorData["ax"] = (int)sample.get(sensorNum).ax;
                    sensorData["ay"] = (int)sample.get(sensorNum).ay;
                    sensorData["az"] = (int)sample.get(sensorNum).az;
                    sensorData["gx"] = (int)sample.get(sensorNum).gx;
                    sensorData["gy"] = (int)sample.get(sensorNum).gy;
                    sensorData["gz"] = (int)sample.get(sensorNum).gz;
                }
            }
            serializeJson(doc, Serial);
            Serial.println();
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