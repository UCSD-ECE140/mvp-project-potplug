#include <Arduino.h>

#ifndef SAMPLING_H
#define SAMPLING_H

const uint32_t SAMPLE_SIZE = 100;
const uint32_t SAMPLE_PERIOD_US = 1500;
const uint32_t SAMPLE_STACK_DEPTH = 4000;

enum Sample_Success {NO_SAMPLE, A_SAMPLE, BUF_FULL};

union i32_t {
  uint32_t iValue;
  uint8_t bytes[sizeof(float)];
};

union f32_t {
    float fValue;
    uint8_t bytes[sizeof(float)];
};


#endif