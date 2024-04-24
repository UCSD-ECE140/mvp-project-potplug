#include <Arduino.h>

#ifndef SAMPLING_H
#define SAMPLING_H

const uint32_t SAMPLE_SIZE = 500;
const uint32_t SAMPLE_PERIOD_MS = 10;


enum Sample_Success {NO_SAMPLE, A_SAMPLE, BUF_FULL};
#endif