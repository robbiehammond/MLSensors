#ifndef SINGLESENSORDATA_H 
#define SINGLESENSORDATA_H
#include <Arduino.h>

struct SingleSensorData {
    int sensorNum;
    int16_t ax;
    int16_t ay;
    int16_t az;
    int16_t gx;
    int16_t gy;
    int16_t gz;

    std::string to_string() {
        std::string s;
        s += "{\n";
        s += "\tData from Sensor Number" + std::to_string(sensorNum) + "\n";
        s += "\tax:" + std::to_string(ax) + "\n";
        s += "\tay:" + std::to_string(ay) + "\n";
        s += "\taz:" + std::to_string(az) + "\n";
        s += "\tgx:" + std::to_string(gx) + "\n";
        s += "\tgy:" + std::to_string(gy) + "\n";
        s += "\tgz:" + std::to_string(gz) + "\n";
        s += "}\n";
        return s;
    }
};
#endif