#include "Comms.h"

uint8_t Comms::isConnected() {
    return connected;
}

void Comms::setup() {
    #if BT
    Serial.begin(DEVICE_NAME);
    while(!Serial.connected()){}
    #else
    Serial.begin(115200);
    #endif
}

void Comms::send_data(dist_data& dist, gyro_data& gyro) {
    send_label(BEGIN_DATA);
    end_line();

    send_samples(DIST_TIME, dist.time);
    send_samples(DIST, dist.distance);

    send_samples(GRYO_TIME, gyro.time);
    send_samples(ACC_X, gyro.a_x);
    send_samples(ACC_Y, gyro.a_y);
    send_samples(ACC_Z, gyro.a_z);
    send_samples(W_X, gyro.w_x);
    send_samples(W_Y, gyro.w_y);
    send_samples(W_Z, gyro.w_z);

    send_label(END_DATA);
    end_line();
    
}

void Comms::send_samples(const char* label, i32_t* data) {
    send_label(label);
    Serial.print(':');
    Serial.print('i');
    Serial.print(':');
    Serial.print(data[0].iValue);
    for(int i = 1; i < SAMPLE_SIZE; i++) {
        Serial.print(',');
        Serial.print(data[i].iValue);
    }
    end_line();
}

void Comms::send_samples(const char* label, f32_t* data) {
    send_label(label);
    Serial.print(':');
    Serial.print('f');
    Serial.print(':');
    Serial.print(data[0].fValue);
    for(int i = 1; i < SAMPLE_SIZE; i++) {
        Serial.print(',');
        Serial.print(data[i].fValue);
    }
    end_line();

}

void Comms::send_label(const char* label) {
    Serial.print(label);
}

void Comms::end_line() {
    Serial.println();
}
