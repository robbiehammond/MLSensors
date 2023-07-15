#ifndef ACTION_H
#define ACTION_H
#include <queue>
#include <Arduino.h>
#include <SensorState.h>
#include <WriteOptions.h>

//A series of samples that can be used to determine if a keypress happened within these samples.
class Action {
public:
    Action();
    void setStates(std::array<SensorState, SAMPLES_PER_ACTION>& capturedSamples);
    void writeOut(WriteOption w);

private:
    std::array<SensorState, SAMPLES_PER_ACTION> lastSamples;
};

#endif