#include <Arduino.h>

#ifndef DISTANCE_H
#define DISTANCE_H

#define SAMPLE_SIZE 500

enum Sample_Success {NO_SAMPLE, A_SAMPLE, BUF_FULL};

struct dist_data {
  uint32_t time;
  uint32_t distance;
};

struct DistanceSensor {
    uint8_t trigger;
    uint8_t echo;

    dist_data dist_buf_1[SAMPLE_SIZE];
    dist_data dist_buf_2[SAMPLE_SIZE];
    dist_data *dist_rec = dist_buf_1;
    dist_data *dist_save = dist_buf_2;

    uint8_t data_ready = false;

    void swap_buf();
    Sample_Success sample(const uint8_t period);
    void setup(uint8_t trigger_pin, uint8_t echo_pin);
};


#endif