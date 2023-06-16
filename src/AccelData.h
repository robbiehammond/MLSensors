#ifndef ACCELDATA_H
#define ACCELDATA_H

const static int SAMPLES_PER_ACTION = 10;
struct AccelData {
    int ax;
    int ay;
    int az;
    int gx;
    int gy;
    int gz;
};
#endif