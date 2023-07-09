#include <MPU6050.h>
#include <queue>
#include "Action.h"

MPU6050 sensor; //The sensor that is currently being looked at
int16_t rawVals[6]; //Where raw data is read to
SensorState curState; //Written to over and over again for a copy to get pushed into samples.
std::array<SensorState, SAMPLES_PER_ACTION> capturedStates; //After button press, these are the previous (and current) states that get sent over.
Action curAction; //When a button press happens, it's stored here.
int sampleInd = 0; //loops through capturedSamples updating them every loop
bool enoughSamplesCollected = false; //turns true when we have 10 samples collected 
long int lastInit = millis();

//Sensor reads will come from the input sensor number.
//HIGH = address is now 0x69, low means it's 0x68.
//Device we want will be on 0x68.
void changeSensor(int sensorNum) {
    switch (sensorNum) {
        case 0:
            digitalWrite(SENSOR0PIN, LOW);
            digitalWrite(SENSOR1PIN, HIGH);
            digitalWrite(SENSOR2PIN, HIGH);
            digitalWrite(SENSOR3PIN, HIGH);
            break;
        case 1:
            digitalWrite(SENSOR0PIN, HIGH);
            digitalWrite(SENSOR1PIN, LOW);
            digitalWrite(SENSOR2PIN, HIGH);
            digitalWrite(SENSOR3PIN, HIGH);
            break;
        case 2:
            digitalWrite(SENSOR0PIN, HIGH);
            digitalWrite(SENSOR1PIN, HIGH);
            digitalWrite(SENSOR2PIN, LOW);
            digitalWrite(SENSOR3PIN, HIGH);
            break;
        case 3:
            digitalWrite(SENSOR0PIN, HIGH);
            digitalWrite(SENSOR1PIN, HIGH);
            digitalWrite(SENSOR2PIN, HIGH);
            digitalWrite(SENSOR3PIN, LOW);
            break;
        default:
            const std::string s = "Invalid pin passed: " + std::to_string(sensorNum);
            Serial.println(s.c_str());
    }
}

//read current sensor data, compile it into the SensorSample. After this is called, the curSample has the most up-to-date data.
void updateSensorData() {
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {

        //make the variable sensor reference the correct physical sensor
        changeSensor(sensorNum); 

        //get values from that sensor
        sensor.getMotion6(&rawVals[iAx], &rawVals[iAy], &rawVals[iAz], 
                          &rawVals[iGx], &rawVals[iGy], &rawVals[iGz]);


        //store those values in curState for that sensor.
        curState.set(sensorNum, rawVals);
    };
}

//Give it it's timestamp of when it was taken, and put it into the capturedSamples list.
void recordSensorData() {
    curState.markAsCompleted();
    capturedStates[sampleInd] = curState;
    curState.resetState();
}


/*
Loop through all the sensors and check their most recently recorded y acceleration. If it abruptly changes 
in whatever direction is up, it was probably a keypress.

Probably could just be done immediately in updateSensorData() so we don't need to loop over everything again. Eh it's probably fine.
*/
bool possiblePress() {
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
        int16_t curXAcc = curState.get(sensorNum).ax;
        int16_t curYAcc = curState.get(sensorNum).ay;
        int16_t curZAcc = curState.get(sensorNum).az;
        // not just y! You can tilt the device and stuff too!
        float mag = sqrt(curXAcc * curXAcc + curYAcc * curYAcc + curZAcc * curZAcc);


        //TODO: Make this dependent on the magnitude rather than 
        if (curXAcc >= THRESHOLD || curYAcc >= THRESHOLD || curZAcc >= THRESHOLD) {
            return true;
        }

    }
    return false;
}

void reinit() {
    if (millis() - lastInit >= REINIT_TIME) {
        for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
            changeSensor(sensorNum);
            sensor.initialize();
            bool connected = sensor.testConnection();
            if (connected)
                sensor.setFullScaleAccelRange(MPU6050_ACCEL_FS_16);
            else
                Serial.println("Not connected, even on reinit call");
        }
        lastInit = millis();
    }
}


void setup() {
    Serial.begin(BAUD_RATE);
    pinMode(SENSOR0PIN, OUTPUT);
    pinMode(SENSOR1PIN, OUTPUT);
    pinMode(SENSOR2PIN, OUTPUT);
    pinMode(SENSOR3PIN, OUTPUT);

    //All disiabled initially.
    digitalWrite(SENSOR0PIN, HIGH);
    digitalWrite(SENSOR1PIN, HIGH);
    digitalWrite(SENSOR2PIN, HIGH);
    digitalWrite(SENSOR3PIN, HIGH);
    Wire.begin();

    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
        changeSensor(sensorNum);
        sensor.initialize();
        Serial.println(sensor.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));
        sensor.setFullScaleAccelRange(MPU6050_ACCEL_FS_16);
    }

}

/*
For 1 sensor, normally executes in 1-2 ms (between 500 Hz and 1 kHz), but when it's time to print,
it takes around 16-17 ms.

For 4 sensors, normally executes in 6-7 ms, but when it's time to print,
it takes about 50-52 ms.
*/
void loop() {
    if (!enoughSamplesCollected && sampleInd == (SAMPLES_PER_ACTION - 1)) enoughSamplesCollected = true;
    long int t = millis();


    updateSensorData();

    recordSensorData();

    //if we're actively sending messages, collected enough samples, and a press is detected
    if (enoughSamplesCollected && possiblePress()) {

        curAction.setStates(capturedStates);
        curAction.writeOut(WriteOption::SERIAL_OUT);
    }
    if (SHOULD_PERIODICALLY_REINIT) {
        reinit();
    }
    sampleInd = (sampleInd + 1) % SAMPLES_PER_ACTION;
    //Serial.println(millis() - t);
}