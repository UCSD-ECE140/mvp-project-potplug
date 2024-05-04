## I'm using this file to demonstrate a Pythonic versio of what our data
## packets will look like coming from the ESP-32.
## Author: Henri

esp32_to_phone_data_packet = {
  "time" :  [   0,   1,   2,   3], # timestamp of measurment in milliseconds relative to arduino start (used for sampling purposes, not actually tracking time)
  "acc_x" : [   0,   1,   2,   3], # acceleration in x direction (m/s^2)
  "acc_y" : [   0,   1,   2,   3], # acceleration in y direction (m/s^2)
  "acc_z" : [   0,   1,   2,   3], # acceleration in z direction (m/s^2)
  "w_x"   : [   0,   1,   2,   3], # angular acceleration about x axis (rad/s^2)
  "w_x"   : [   0,   1,   2,   3], # angular acceleration about y axis (rad/s^2)
  "w_z"   : [   0,   1,   2,   3], # angular acceleration about z axis (rad/s^2)
  "dist"  : [   0,   1,   2,   3] # distance of sensor (cm)
}