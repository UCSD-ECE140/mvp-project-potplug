#include "Process.h"

uint8_t process_data(DistanceSensor& ds, GyroSensor& gs)
{
    static const uint8_t dist_cutoff = 5;
    uint32_t last_distance = ds.save->distance[0].iValue;
    uint32_t current_distance;
    uint32_t difference;
    uint8_t pothole_flag = 0;
    for (uint32_t i = 1; i < SAMPLE_SIZE; i++)
    {
        // Set flag if sudden change in distance
        current_distance = ds.save->distance[i].iValue;
        difference = current_distance > last_distance ? current_distance - last_distance : last_distance - current_distance;
        // Serial.println(current_distance);

        if (difference > dist_cutoff)
        {   
            pothole_flag = 1;
            break;
        }
        last_distance = current_distance;
    }
    if (pothole_flag == 1)
    {
        // Serial.println("Pothole flagged");
        comms.send_data(*ds.save, *gs.save);
    }
    uint16_t time_elapsed = ds.save[SAMPLE_SIZE - 1].time - ds.save[0].time;
    return pothole_flag;
}
