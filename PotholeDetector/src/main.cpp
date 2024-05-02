#include <Arduino.h>
#include "Distance.h"
#include "Process.h"
#include "Gyro.h"

const uint8_t trig_pin = 33;
const uint8_t echo_pin = 32;

static DistanceSensor d_sensor;
static GyroSensor g_sensor;
TaskHandle_t *distance_task;
TaskHandle_t *gyro_task;

TaskHandle_t *process_data_task;
SemaphoreHandle_t data_process;

void process(void *p)
{
    while (1)
    {
        if(uxSemaphoreGetCount(data_process) == 2) {
            xSemaphoreTake(data_process, 0);
            xSemaphoreTake(data_process, 0);
            process_data(d_sensor, g_sensor);
        }
        vTaskDelay(SAMPLE_PERIOD_MS * SAMPLE_SIZE / 10 / portTICK_PERIOD_MS);
    }
}

void sample_distance(void *p)
{
    d_sensor.setup(trig_pin, echo_pin);
    while (1)
    {
        if (BUF_FULL == d_sensor.sample(SAMPLE_PERIOD_MS))
        {
            xSemaphoreGive(data_process);
        }
        vTaskDelay(SAMPLE_PERIOD_MS / portTICK_PERIOD_MS);
    }
}

void sample_gyro(void *p)
{
    g_sensor.setup();
    while (1)
    {
        if (BUF_FULL == g_sensor.sample(SAMPLE_PERIOD_MS))
        {
            xSemaphoreGive(data_process);
        }
        vTaskDelay(SAMPLE_PERIOD_MS / portTICK_PERIOD_MS);
    }
}

void setup()
{
    Serial.begin(115200);
    data_process = xSemaphoreCreateCounting(2, 0);

    xTaskCreate(
        sample_distance,
        "Sample Sensors",
        4000,
        NULL,
        1,
        distance_task);

    xTaskCreate(
        sample_gyro,
        "Sample Gyro",
        4000,
        NULL,
        1,
        gyro_task);

    xTaskCreate(
        process,
        process_name,
        process_stack_depth,
        NULL,
        1,
        process_data_task);

    vTaskDelete(NULL);
}

// Never reached
void loop()
{
}
