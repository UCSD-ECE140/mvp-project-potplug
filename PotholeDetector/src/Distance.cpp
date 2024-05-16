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

Sample_Success DistanceSensor::sample()
{
    static uint32_t i = 0;
    uint32_t current_time = millis();
    Sample_Success result = A_SAMPLE;

    if (i >= SAMPLE_SIZE)
    {
        swap_buf();
        i = 0;
        result = BUF_FULL;
    }

    uint32_t distance;
    digitalWrite(trigger, HIGH);
    delayMicroseconds(2);
    digitalWrite(trigger, LOW);
    distance = pulseIn(echo, HIGH, 100000);
    distance = (distance/2) / 29.1;

    rec->save(i, current_time, distance);
    i += 1;
    return result;
}

void dist_data::save(uint32_t i, uint32_t _time, uint32_t _dist) {
    time[i].iValue = _time;
    distance[i].iValue = _dist;
}

