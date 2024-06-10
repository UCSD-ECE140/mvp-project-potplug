#include "Gyro.h"

  void GyroSensor::setup() {
    if (!gyro.begin()) {
        Serial.println("Failed to set up!");
    }
    else {
      Serial.println("Gyro set up successfully!");
    }
    gyro.setAccelerometerRange(MPU6050_RANGE_8_G);
    gyro.setGyroRange(MPU6050_RANGE_500_DEG);
    gyro.setFilterBandwidth(MPU6050_BAND_21_HZ);
  }

  Sample_Success GyroSensor::sample() {
    static sensors_event_t a, g, temp;
    static uint32_t i = 0;
    uint32_t current_time = millis();
    Sample_Success result = A_SAMPLE;

    if(i >= SAMPLE_SIZE) {
        swap_buf();
        i = 0;
        result = BUF_FULL;
    }
    gyro.getEvent(&a, &g, &temp);
    rec->save(i, current_time, a.acceleration.x, a.acceleration.y, a.acceleration.z, g.gyro.x, g.gyro.y, g.gyro.z, temp.temperature);
    i += 1;
    return result;
  }

  void GyroSensor::swap_buf() {
        gyro_data *temp = rec;
        rec = save;
        save = temp;
  }

    void gyro_data::save(uint32_t i, uint32_t _time, float _ax, float _ay, float _az, float _wx, float _wy, float _wz, float _temp) {
      time[i] = _time;
      a_x[i] = _ax;
      a_y[i] = _ay;
      a_z[i] = _az;
      w_x[i] = _wx;
      w_y[i] = _wy;
      w_z[i] = _wz;
      temp[i] = _temp;
    }

