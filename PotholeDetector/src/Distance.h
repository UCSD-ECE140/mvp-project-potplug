#include <Arduino.h>
#include "Sampling.h"
#include "Process.h"

#ifndef DISTANCE_H
#define DISTANCE_H


struct dist_data {
    i32_t 
      time[SAMPLE_SIZE],
      distance [SAMPLE_SIZE];
    void save(uint32_t i, uint32_t _time, uint32_t _dist);
};

struct DistanceSensor {
    uint8_t trigger;
    uint8_t echo;

    dist_data dist_buf_1;
    dist_data dist_buf_2;
    dist_data *rec = &dist_buf_1;
    dist_data *save = &dist_buf_2;

    uint8_t pothole_flag = 0;
    uint8_t process_flag = 0;

    void swap_buf();
    Sample_Success sample();
    void setup(uint8_t trigger_pin, uint8_t echo_pin);
};

#endif