#include <MPU6050.h>
#include <queue>
#include "Action.h"

MPU6050 accelgyro;
int16_t rawVals[6];
const int iAx = 0;
const int iAy = 1;
const int iAz = 2;
const int iGx = 3;
const int iGy = 4;
const int iGz = 5;
std::queue<AccelData> q;
std::array<AccelData, SAMPLES_PER_ACTION> ar; 



void setup() {
    accelgyro.getMotion6(&rawVals[iAx], &rawVals[iAy], &rawVals[iAz], 
                             &rawVals[iGx], &rawVals[iGy], &rawVals[iGz]);
}


void loop() {
    accelgyro.getMotion6(&rawVals[iAx], &rawVals[iAy], &rawVals[iAz], 
                             &rawVals[iGx], &rawVals[iGy], &rawVals[iGz]);

    AccelData a = {
        rawVals[iAx],
        rawVals[iAy], 
        rawVals[iAz],
        rawVals[iGx],
        rawVals[iGy], 
        rawVals[iGz]
    };

    q.push(a);

    if (q.size() == SAMPLES_PER_ACTION) {
        for (int i = 0; i < SAMPLES_PER_ACTION; i++) {
            ar[i] = q.front();
            q.pop();
        }

        Action action(ar);
        if (action.likelyContainsButtonPress())
            action.writeOut(WriteOption::SERIAL_OUT);
    }
}