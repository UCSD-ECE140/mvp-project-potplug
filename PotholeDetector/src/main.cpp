#include <Arduino.h>
#include "Distance.h"
#include "Process.h"
#include "Gyro.h"

const uint8_t trig_pin = 33;
const uint8_t echo_pin = 32;

static DistanceSensor d_sensor;
// static GyroSensor g_sensor;
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

void sample_sensors(void *p)
{
    static uint8_t buf_filled = 0;
    d_sensor.setup(trig_pin, echo_pin);
    static uint32_t last_sample = millis();
    static uint32_t current_time;
    while (1)
    {
        if (BUF_FULL == d_sensor.sample())
        {
            xSemaphoreGive(data_process);
        }
        vTaskDelay(SAMPLE_PERIOD_MS / portTICK_PERIOD_MS);
    }
}

void setup()
{
    Serial.begin(115200);
    data_process = xSemaphoreCreateBinary();
    xSemaphoreTake(data_process, 0);

    xTaskCreate(
        sample_sensors,
        "Sample Sensors",
        900000,
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
