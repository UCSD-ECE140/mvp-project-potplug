#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include "Sampling.h"

#ifndef GYRO_H
#define GYRO_H

void sample_gyro(void *p);
void setup_gyro();

struct gyro_data
{
  uint32_t time;
  float
      a_x,
      a_y,
      a_z,
      w_x,
      w_y,
      w_z,
      temp;
};

struct GyroSensor
{
  Adafruit_MPU6050 gyro;

  void setup();
  Sample_Success sample(const uint8_t period_ms);
  void swap_buf();

  gyro_data dist_buf_1[SAMPLE_SIZE];
  gyro_data dist_buf_2[SAMPLE_SIZE];
  gyro_data *rec = dist_buf_1;
  gyro_data *save = dist_buf_2;
};

#endif