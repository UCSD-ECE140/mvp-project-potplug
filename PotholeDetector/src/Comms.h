// #include <BLEDevice.h>
// #include <BLEUtils.h>
// #include <BLEServer.h>
// #include <Arduino.h>
#include <BluetoothSerial.h>
#include "Distance.h"
#include "Gyro.h"
#include "Sampling.h"

// #define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
// #define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
// #define BAUD_RATE 115200

#define BT 1
#define DEVICE_NAME "PotholeDetector"

static struct Comms
{
private:
    uint8_t connected = 0;

#if BT
    BluetoothSerial SerialBt;
    // BLEServer *pServer;
    // BLEService *pService;
    // BLECharacteristic *pCharacteristic;
    // BLEAdvertising *pAdvertising;
#endif

public:
    void setup();
    void send(dist_data* data);
    void send(gyro_data* data);
    void send(uint8_t* data);
    void Comms::send(uint8_t *label, uint8_t label_len, uint32_t* data, size_t data_len);
    uint8_t isConnected();
} comms;
