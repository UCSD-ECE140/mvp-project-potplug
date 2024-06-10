#include "Process.h"
#include <cmath>

using namespace std;

uint8_t process_data(GyroSensor &gs, DistanceSensor &ds)
{
#if ALWAYS_SEND

    comms.send_data(*gs.save, *ds.save);
    return 1;

#else
    static const uint8_t dist_cutoff = 5;
    uint32_t last_distance = ds.save->distance[0];
    float last_accel = gs.save->a_z[0];
    float current_accel;
    uint32_t current_distance;
    uint32_t distance_difference;
    float accel_difference;
    uint8_t pothole_flag = 0;
    for (uint32_t i = 1; i < SAMPLE_SIZE; i++)
    {
        current_distance = ds.save->distance[i];
        distance_difference = current_distance > last_distance ? current_distance - last_distance : last_distance - current_distance;
        if (distance_difference > dist_cutoff)
        {
            pothole_flag = 1;
            break;
        }
        current_accel = gs.save->a_z[i];
        accel_difference = current_accel > last_accel ? current_accel - last_accel : last_accel - current_accel;
        Serial.println(accel_difference);
        if (accel_difference > 1)
        {
            pothole_flag = 1;
            Serial.println("Incident flagged");
            break;
        }
        last_distance = current_distance;
        last_accel = current_accel;
    }
    if (pothole_flag == 1)
    {
        comms.send_data(*gs.save, *ds.save);
    }
    return pothole_flag;
#endif
}
