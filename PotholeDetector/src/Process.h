#include <Arduino.h>
#include "Distance.h"

#ifndef PROCESS_H
#define PROCESS_H

const uint32_t process_stack_depth = 10000;
const char process_name[] = "Process Data";

uint8_t process_distance(DistanceSensor ds);

#endif