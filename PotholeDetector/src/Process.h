#ifndef PROCESS_H
#define PROCESS_H

#include <Arduino.h>
#include "Sampling.h"
#include "Distance.h"
#include "Gyro.h"

const uint32_t process_stack_depth = 10000;
const char process_name[] = "Process Data";
const uint32_t dist_cutoff = 500;

uint8_t process_data(DistanceSensor &ds, GyroSensor &gs);


#endif