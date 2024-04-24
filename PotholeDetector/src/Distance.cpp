#include "Distance.h"

void DistanceSensor::setup(uint8_t trigger_pin, uint8_t echo_pin)
{
    trigger = trigger_pin;
    echo = echo_pin;
    pinMode(trigger, OUTPUT);
    pinMode(echo, INPUT);
    digitalWrite(trigger, LOW);
}

void DistanceSensor::swap_buf()
{
    dist_data *temp = rec;
    rec = save;
    save = temp;
}

Sample_Success DistanceSensor::sample(const uint8_t period_ms)
{
    static uint32_t i = 0;
    uint32_t current_time = millis();
    Sample_Success result = A_SAMPLE;
    static portMUX_TYPE port = portMUX_INITIALIZER_UNLOCKED;

    if (i >= SAMPLE_SIZE)
    {
        swap_buf();
        i = 0;
        result = BUF_FULL;
    }

    uint32_t distance;
    taskENTER_CRITICAL(&port);
    digitalWrite(trigger, HIGH);
    delayMicroseconds(2);
    digitalWrite(trigger, LOW);
    distance = pulseIn(echo, HIGH, 10000000);
    taskEXIT_CRITICAL(&port);
    distance *= 0.343 / 2;

    rec[i] = {current_time, distance};
    i += 1;
    vTaskDelay(period_ms / portTICK_PERIOD_MS);
    return result;
}
