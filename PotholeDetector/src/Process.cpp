#include "Process.h"

uint8_t process_data(DistanceSensor& ds, GyroSensor& gs)
{
    static const uint32_t cutoff = 50;
    uint32_t last_distance = ds.save[0].distance;
    uint32_t current_distance;
    uint32_t difference;
    uint8_t pothole_flag = 0;
    for (uint16_t i = 1; i < SAMPLE_SIZE; i++)
    {
        current_distance = ds.save[i].distance;
        difference = current_distance > last_distance ? current_distance - last_distance : last_distance - current_distance;
        Serial.println(current_distance);

        if (difference > cutoff)
        {   
            pothole_flag = 1;
            break;
        }
        last_distance = current_distance;
    }
    if (pothole_flag == 1)
    {
        Serial.println("Potential pothole!");
    }
    uint16_t time_elapsed = ds.save[SAMPLE_SIZE - 1].time - ds.save[0].time;
    Serial.print("ms elapsed: ");
    Serial.println(time_elapsed);
    return pothole_flag;
}
