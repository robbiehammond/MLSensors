#ifndef SENSORDATA_H
#define SENSORDATA_H
#include <SingleSensorData.h>
#include <unordered_map>
#include "MPU6050.h"
#include "constants.h"

//1 Sensor Sample = (data from sensor0, data from sensor1, data from sensorN) all at a specific point in time.
class SensorState {
public:
    void set(int sensorNum, int16_t* rawData) {
        if (!readyToBeWrittenTo) {
            Serial.println("WRITING TO FINIALIZED SAMPLE");
            return;
        }

        data[sensorNum] = (SingleSensorData) {
            .sensorNum = sensorNum,
            .ax = rawData[iAx],
            .ay = rawData[iAy],
            .az = rawData[iAz],
            .gx = rawData[iGx],
            .gy = rawData[iGy],
            .gz = rawData[iGz]
        };
    }

    SingleSensorData get(int sensorNum) {
        return data[sensorNum];
    }

    std::string to_string() {
        std::string s;
        s += "----------------\n";
        s += "Sample Taken at " + std::to_string(timeWhenTaken) + "\n";
        for (int i = 0; i < NUM_SENSORS; i++) {
            auto& sensorData = data[i];
            s += sensorData.to_string();
        }
        s += "----------------\n";
        s += "\n";
        s += "\n";
        return s;
    }

    long int getTimeStamp() {
        return timeWhenTaken;
    }

    void markAsCompleted() {
        timeWhenTaken = millis();
        readyToBeWrittenTo = false;
    }

    void resetState() {
        readyToBeWrittenTo = true;
    }

private:
    bool readyToBeWrittenTo = true;
    std::array<SingleSensorData, NUM_SENSORS> data;
    long int timeWhenTaken;
};

#endif