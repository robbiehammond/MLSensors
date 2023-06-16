#ifndef ACTION_H
#define ACTION_H
#include <queue>
#include <Arduino.h>
#include <SensorSample.h>
#include <WriteOptions.h>

//A series of samples that can be used to determine if a keypress happened within these samples.
class Action {
public:
    Action(std::queue<SensorSample>& capturedSamples);
    bool likelyContainsButtonPress();
    void writeOut(WriteOption w);

private:
    std::array<SensorSample, SAMPLES_PER_ACTION> lastSamples;
};

#endif