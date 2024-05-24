#include "Process.h"

uint8_t process_data(GyroSensor &gs, DistanceSensor &ds)
{
#if ALWAYS_SEND

    comms.send_data(*gs.save, *ds.save);
    return 1;

#else
    static const uint8_t dist_cutoff = 5;
    uint32_t last_distance = ds.save->distance[0];
    uint32_t current_distance;
    uint32_t difference;
    uint8_t pothole_flag = 0;
    for (uint32_t i = 1; i < SAMPLE_SIZE; i++)
    {
        current_distance = ds.save->distance[i];
        difference = current_distance > last_distance ? current_distance - last_distance : last_distance - current_distance;

        if (difference > dist_cutoff)
        {
            pothole_flag = 1;
            break;
        }
        last_distance = current_distance;
    }
    if (pothole_flag == 1)
    {
        comms.send_data(*gs.save, *ds.save);
    }
    return pothole_flag;
#endif
}
