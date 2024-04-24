#include <Arduino.h>
#include "Distance.h"
#include "Process.h"

// SAMPLING VARS
const int SAMPLE_PERIOD_MS = 1;

// DISTANCE SENSING

const uint8_t trig_pin = 33;
const uint8_t echo_pin = 32;

static DistanceSensor d_sensor;
TaskHandle_t *distance_task;
TaskHandle_t *process_data_task;
SemaphoreHandle_t data_process;

void process(void *p)
{
  while (1)
  {
    if (xSemaphoreTake(data_process, 0) == pdTRUE)
    {
      process_distance(d_sensor);
    }
  }
}

void measure_distance(void *p)
{
  d_sensor.setup(trig_pin, echo_pin);
  while (1)
  {
    if (BUF_FULL == d_sensor.sample(SAMPLE_PERIOD_MS))
    {
      Serial.println("Buffer filled");
      xSemaphoreGive(data_process);
    }
  }
}

// GYRO SENSING

struct gyro_data
{
  uint32_t time;
  float
      a_x,
      a_y,
      a_z,
      w_x,
      w_y,
      w_z;
};

uint32_t gyro_buf_1[SAMPLE_SIZE];
uint32_t gyro_buf_2[SAMPLE_SIZE];
uint32_t *gryo_rec = gyro_buf_1;
uint32_t *gryo_save = gyro_buf_2;

void setup()
{
  Serial.begin(115200);
  data_process = xSemaphoreCreateBinary();
  xSemaphoreTake(data_process, 0);

  xTaskCreate(
      measure_distance,
      "Distance Sensor 1",
      40000,
      NULL,
      1,
      distance_task);

  xTaskCreate(
      process,
      process_name,
      process_stack_depth,
      NULL,
      1,
      process_data_task);

  vTaskDelete(NULL);
}

void loop()
{
  // put your main code here, to run repeatedly:
}
