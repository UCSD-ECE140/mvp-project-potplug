#include <Arduino.h>

#ifndef GYRO_H
#define GYRO_H

void sample_gyro(void *p);
void setup_gyro(void *p);

struct dist_data {
  uint32_t time;
  uint32_t distance;
};

#endif