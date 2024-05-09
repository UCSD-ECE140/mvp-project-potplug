import serial
import pandas as pd
import numpy as np
from IPython.display import display
import struct

class SerialHandler():
  ser = None
  df : pd.DataFrame
  msg_count : int
  
  def __init__(self, _df : pd.DataFrame = None) -> None:
    self.ser = serial.Serial(port="COM5")
    self.df = pd.DataFrame() if _df == None else _df
    self.msg_count = 0
  
  def receive_data_packet(self):
    message = self.ser.read_until(b"END")
    message = message.decode()
    self.parse_data_packet(message)
    self.msg_count += 1
    
  def parse_data_packet(self, message : str):
    entry = {}
    lines = message.split('\n')
    for line in lines:
      line = line.strip()
      if ':' in line:
        (label, dtype, data) = line.split(':')
        data = data.split(',')
        entry[label] = data
    entry['message'] = [self.msg_count for i in range(0, len(entry['DST']))]
    self.df = pd.concat([self.df, pd.DataFrame.from_dict(entry)])
    
  def run(self):
    if self.ser.in_waiting != 0:
      if self.ser.readline().decode().startswith("BGD"):
        self.receive_data_packet()
      
  def close(self):
    self.ser.close()

    
if __name__ == '__main__':
  try:
    serial = SerialHandler()
    print('Setup done')
    prev_count = 0
    while True:
      serial.run()
      if serial.msg_count != prev_count:
        display(serial.df)
        prev_count = serial.msg_count
  finally:
    serial.close()
    print("Comms closed")
          
        
    
