#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include "Sampling.h"

#ifndef GYRO_H
#define GYRO_H

struct gyro_data
{
  i32_t 
      time[SAMPLE_SIZE];
  f32_t
      a_x [SAMPLE_SIZE],
      a_y [SAMPLE_SIZE],
      a_z [SAMPLE_SIZE],
      w_x [SAMPLE_SIZE],
      w_y [SAMPLE_SIZE],
      w_z [SAMPLE_SIZE],
      temp [SAMPLE_SIZE];
  void save(uint32_t index, uint32_t _time, float _ax, float _ay, float _az, float _wx, float _wy, float _wz, float _temp);
};


struct GyroSensor
{
  Adafruit_MPU6050 gyro;

  void setup();
  Sample_Success sample();
  void swap_buf();

  gyro_data buf_1;
  gyro_data buf_2;
  gyro_data *rec = &buf_1;
  gyro_data *save = &buf_2;
};



#endif