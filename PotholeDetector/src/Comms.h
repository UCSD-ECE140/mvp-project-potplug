
#ifndef COMMS_H
#define COMMS_H

#include <BluetoothSerial.h>
#include "Gyro.h"
#include "Sampling.h"
#include "Distance.h"

#define BT 0 // 1 - Bluetooth on.   0 - communicate over serial
#define DEVICE_NAME "Detector1"

#define BEGIN_DATA "BGD"
#define END_DATA "END"
#define TIME "TME"
#define GRYO_TIME "GYT"
#define DIST_TIME "DST"
#define ACC_X "ACX"
#define ACC_Y "ACY"
#define ACC_Z "ACZ"
#define W_X "RTX"
#define W_Y "RTY"
#define W_Z "RTZ"
#define DIST "DIS"

static const uint8_t LABEL_LENGTH = 4;


struct Comms
{
    uint8_t connected = 0;
    void end_line();

#if BT
    BluetoothSerial Serial;

#endif

    void setup();
    void send_data(gyro_data &gyro, dist_data& dist);
    void send_samples(const char* label, uint32_t* data);
    void send_samples(const char* label, float* data);
    void send_label(const char *label);
    uint8_t isConnected();
};

static Comms comms;

#endif