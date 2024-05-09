/* Simple data measurements and processing on ESP32 for ultrasound and IMU
 * Runs sampling on core 0 and processing on core 1
 */

#include <Arduino.h>
#include "Process.h"
#include "Sampling.h"
#include "Comms.h"

// Constants
enum Cores
{
    CORE_0,
    CORE_1
};

// Sensor sampling task
void sample_sensors(void *p);
TaskHandle_t *sensor_sampling;
static DistanceSensor d_sensor;
static GyroSensor g_sensor;

// Data processing task
TaskHandle_t *processing;
void process(void *p);

// Tracks whether data is ready to be processed
SemaphoreHandle_t data_process;

void setup()
{
    // Seup comms and wait until connnected
    comms.setup();

    // Set data_process semaphore to 0
    data_process = xSemaphoreCreateBinary();
    xSemaphoreTake(data_process, 0);

    // Pin sampling to Core 0
    xTaskCreatePinnedToCore(
        sample_sensors,
        "Sample Sensors",
        SAMPLE_STACK_DEPTH,
        NULL,
        0,
        sensor_sampling,
        CORE_0);

    // Pin processing to Core 1
    xTaskCreatePinnedToCore(
        process,
        process_name,
        4000,
        NULL,
        0,
        processing,
        CORE_1);

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
            process_data(d_sensor, g_sensor);
        }
    }
}

void sample_sensors(void *p)
{

    // Ultrasound setup
    const uint8_t trig_pin = 33;
    const uint8_t echo_pin = 32;
    d_sensor.setup(trig_pin, echo_pin);
    g_sensor.setup();

    while (1)
    {
        d_sensor.sample();
        if (g_sensor.sample() == BUF_FULL)
        {
            xSemaphoreGive(data_process);
        }
        delayMicroseconds(SAMPLE_PERIOD_US);
    }
}