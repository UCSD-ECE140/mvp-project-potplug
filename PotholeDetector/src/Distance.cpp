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
    int triggerPin = trigger;
    int echoPin = echo;
    noInterrupts(); // Disable interrupts

    // Send trigger pulse
    digitalWrite(triggerPin, LOW);
    delayMicroseconds(2);
    digitalWrite(triggerPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPin, LOW);

    // Wait for echo pulse to start
    while (digitalRead(echoPin) == LOW)
        ;

    // Measure echo pulse length
    uint32_t pulseStart = micros();
    while (digitalRead(echoPin) == HIGH)
        ;
    uint32_t pulseLength = micros() - pulseStart;

    interrupts(); // Re-enable interrupts

    // Calculate distance
    float distance = pulseLength / 58.0;

    rec->save(i, current_time, distance);
    i += 1;
    return result;
}

void dist_data::save(uint32_t i, uint32_t _time, float _dist)
{
    time[i] = _time;
    distance[i] = _dist;
}
