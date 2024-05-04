#include "Comms.h"

uint8_t Comms::isConnected() {
    return connected;
}

#if BT
void Comms::setup() {
    SerialBt.begin(DEVICE_NAME);
}

void Comms::send(dist_data* data) {
    uint32_t d[SAMPLE_SIZE];
    for(int i = 0; i < SAMPLE_SIZE; i++)
        d[i] = data[i].time;
    char time_label[] = "t";
    send(time_label, 1, d, SAMPLE_SIZE);

    for(int i = 0; i < SAMPLE_SIZE; i++)
        d[i] = data[i].distance;
    send('t', 1, d, SAMPLE_SIZE);
}

void Comms::send(char *label, uint8_t label_len, uint32_t* data, size_t data_len) {
    SerialBt.write(label, label_len);
    for(int i = 0; i < SAMPLE_SIZE; i++) {
        SerialBt.write(data[i]);
        SerialBt.write(',');
    }
}

// void Comms::setup()
// {
//     BLEDevice::init("PotholeDetectoe");
//     pServer = BLEDevice::createServer();
//     pService = pServer->createService(SERVICE_UUID);
//     pCharacteristic = pService->createCharacteristic(
//         CHARACTERISTIC_UUID,
//         BLECharacteristic::PROPERTY_READ |
//             BLECharacteristic::PROPERTY_WRITE);

//     pCharacteristic->setValue("Hello World!"); // can send uint8_t via ptr
//     pService->start();

//     pAdvertising = BLEDevice::getAdvertising();
//     pAdvertising->addServiceUUID(SERVICE_UUID);
//     pAdvertising->setScanResponse(true);
//     pAdvertising->setMinPreferred(0x06); // functions that help with iPhone connections issue
//     pAdvertising->setMinPreferred(0x12);
//     BLEDevice::startAdvertising();
// }

#else
void Comms::setup()
{
    Serial.begin(BAUD_RATE);
    connected = 1;
}

#endif
