#include <Arduino.h>
#include "Sampling.h"

#ifndef DISTANCE_H
#define DISTANCE_H

struct dist_data {
  uint32_t time;
  uint32_t distance;
};

struct DistanceSensor {
    uint8_t trigger;
    uint8_t echo;

    dist_data dist_buf_1[SAMPLE_SIZE];
    dist_data dist_buf_2[SAMPLE_SIZE];
    dist_data *rec = dist_buf_1;
    dist_data *save = dist_buf_2;

    uint8_t data_ready = false;

    void swap_buf();
    Sample_Success sample();
    void setup(uint8_t trigger_pin, uint8_t echo_pin);
};


#endif