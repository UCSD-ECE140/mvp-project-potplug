#include <Arduino.h>
#include "Process.h"
#include "Sampling.h"
#include "Comms.h"
#include "Distance.h"

// Constants
enum Cores
{
    CORE_0,
    CORE_1
};

// Distance sensor
DistanceSensor d_sensor;
const uint8_t echo_pin = 32;
const uint8_t trig_pin = 33;

// Sensor sampling task
void sample_sensors(void *p);
TaskHandle_t *sensor_sampling;
static GyroSensor g_sensor;

// Data processing task
TaskHandle_t *processing;
void process(void *p);

// Tracks whether data is ready to be processed
SemaphoreHandle_t data_process;

void setup()
{
    Serial.begin(115200);
    // Setup comms and wait until connnected
    comms.setup();

    // Set data_process semaphore to 0
    data_process = xSemaphoreCreateBinary();
    xSemaphoreTake(data_process, 0);

    xTaskCreate(
        sample_sensors,
        "Sample Sensors",
        SAMPLE_STACK_DEPTH,
        NULL,
        0,
        sensor_sampling);

    xTaskCreate(
        process,
        process_name,
        4000,
        NULL,
        0,
        processing);

    vTaskDelete(NULL);
}

// Never reached
void loop()
{
}

void process(void *p)
{    while (1)
    {
        if (xSemaphoreTake(data_process, portMAX_DELAY))
        {
            process_data(g_sensor, d_sensor);
        }
        vTaskDelay(5 / portTICK_PERIOD_MS);
    }
}

void sample_sensors(void *p)
{
    uint32_t last_sample_time = micros();
    uint32_t current_time;
    d_sensor.setup(trig_pin, echo_pin);
    g_sensor.setup();

    while (1)
    {   current_time = micros();
        if(current_time - last_sample_time >= SAMPLE_PERIOD_US) {
            d_sensor.sample();
            if (g_sensor.sample() == BUF_FULL)
            {
                xSemaphoreGive(data_process);
            }
            last_sample_time = current_time;

        }
    }
}