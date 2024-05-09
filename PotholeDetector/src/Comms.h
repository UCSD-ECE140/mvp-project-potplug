// #include <BLEDevice.h>
// #include <BLEUtils.h>
// #include <BLEServer.h>
// #include <Arduino.h>
#ifndef COMMS_H
#define COMMS_H

#include <BluetoothSerial.h>
#include "Distance.h"
#include "Gyro.h"
#include "Sampling.h"

// #define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
// #define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
// #define BAUD_RATE 115200

#define BT 1 // 1 - Bluetooth on.   0 - communicate over serial
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
    // BLEServer *pServer;
    // BLEService *pService;
    // BLECharacteristic *pCharacteristic;
    // BLEAdvertising *pAdvertising;
#endif

    void setup();
    void send_data(dist_data &data, gyro_data &gyro);
    void send_samples(const char* label, i32_t* data);
    void send_samples(const char* label, f32_t* data);
    void send_label(const char *label);
    uint8_t isConnected();
};

static Comms comms;

#endif