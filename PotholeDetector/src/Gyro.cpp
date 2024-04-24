#include "Gyro.h"

  void GyroSensor::setup() {
    if (!gyro.begin()) {
        Serial.println("Failed to set up!");
    }
    gyro.setAccelerometerRange(MPU6050_RANGE_8_G);
    gyro.setGyroRange(MPU6050_RANGE_500_DEG);
    gyro.setFilterBandwidth(MPU6050_BAND_21_HZ);
  }

  Sample_Success GyroSensor::sample(const uint8_t period_ms) {
    static sensors_event_t a, g, temp;
    static uint32_t i = 0;
    uint32_t current_time = millis();
    Sample_Success result = A_SAMPLE;
    static portMUX_TYPE port = portMUX_INITIALIZER_UNLOCKED;

    if(i >= SAMPLE_SIZE) {
        swap_buf();
        i = 0;
        result = BUF_FULL;
    }
    gyro.getEvent(&a, &g, &temp);
    rec[i] = {current_time, a.acceleration.x, a.acceleration.y, a.acceleration.z, g.gyro.x, g.gyro.y, g.gyro.z, temp.temperature};
    i += 1;
    vTaskDelay(period_ms / portTICK_PERIOD_MS);
    return result;
  }

  void GyroSensor::swap_buf() {
        gyro_data *temp = rec;
        rec = save;
        save = temp;
  }
