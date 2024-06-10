#include "Comms.h"

uint8_t Comms::isConnected() {
    return connected;
}

void Comms::setup() {
    #if BT
    Ser.begin(DEVICE_NAME);
    while(!Ser.connected()) {
        delay(1000);
    }
    #else
    Ser.begin(115200);
    #endif
}

void Comms::send_data(gyro_data& gyro, dist_data& dist) {
    send_label(BEGIN_DATA);
    end_line();

    // send_samples(DIST_TIME, dist.time);
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

void Comms::send_samples(const char* label, uint32_t* data) {
    send_label(label);
    Ser.print(':');
    Ser.print('i');
    Ser.print(':');
    Ser.print(data[0]);
    for(int i = 1; i < SAMPLE_SIZE; i++) {
        Ser.print(',');
        Ser.print(data[i]);
    }
    end_line();
}

void Comms::send_samples(const char* label, float* data) {
    send_label(label);
    Ser.print(':');
    Ser.print('f');
    Ser.print(':');
    Ser.print(data[0]);
    for(int i = 1; i < SAMPLE_SIZE; i++) {
        Ser.print(',');
        Ser.print(data[i]);
    }
    end_line();

}

void Comms::send_label(const char* label) {
    Ser.print(label);
}

void Comms::end_line() {
    Ser.println();
}
