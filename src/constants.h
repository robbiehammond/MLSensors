#ifndef CONSTANTS_H
#define CONSTANTS
static const int BAUD_RATE = 922190;

static const int LHPINKY = 0;
static const int LHRING = 1;
static const int LHMIDDLE = 2;
static const int LHINDEX = 3;
static const int LHTHUMB = 4;

static const int iAx = 0;
static const int iAy = 1;
static const int iAz = 2;
static const int iGx = 3;
static const int iGy = 4;
static const int iGz = 5;

static const int THRESHOLD = 5500;

const static int SAMPLES_PER_ACTION = 20;
const static int NUM_SENSORS = 4; 
const static int DOC_SIZE = 12000;

const static bool SHOULD_PERIODICALLY_REINIT = false; //if somethin comes loose and read is bad, we may need to reinit.
const static int REINIT_TIME = 1000; //reinit after 1 second (1000 ms)

const static int SENSOR0PIN = 26;
const static int SENSOR1PIN = 25;
const static int SENSOR2PIN = 13;
const static int SENSOR3PIN = 12;
#endif