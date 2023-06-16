#ifndef ACTION_H
#define ACTION_H
#include <array>
#include <Arduino.h>
#include <AccelData.h>
#include <WriteOptions.h>
class Action {
public:
    Action(std::array<AccelData, SAMPLES_PER_ACTION> lastSamples);
    bool likelyContainsButtonPress();
    void writeOut(WriteOption w);

private:
    std::array<AccelData, SAMPLES_PER_ACTION> lastSamples;
};

#endif