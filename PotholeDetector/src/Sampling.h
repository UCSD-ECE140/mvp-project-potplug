#include <Arduino.h>

#ifndef SAMPLING_H
#define SAMPLING_H

const uint32_t SAMPLE_SIZE = 250;
const uint32_t SAMPLE_PERIOD_US = 2500;
const uint32_t SAMPLE_STACK_DEPTH = 4000;

enum Sample_Success {NO_SAMPLE, A_SAMPLE, BUF_FULL};


#endif