import serial
import pandas as pd
import numpy as np
from IPython.display import display
from datetime import datetime
from PotholeDataExploration import describe_data

class SerialHandler():
  ser = None
  df : pd.DataFrame
  msg_count : int
  filename : str
  
  bluetooth = "COM5"
  
  def __init__(self, _df : pd.DataFrame = None) -> None:
    self.ser = serial.Serial(port=self.bluetooth)
    self.df = pd.DataFrame() if _df == None else _df
    self.msg_count = 0
    self.filename = f"PotholeData/{datetime.now().strftime('%d_%m_%Y_T%H_%M_%S')}.csv"

  
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
        entry[label] = [float(datum) for datum in data]
    entry['message'] = [self.msg_count for i in range(0, len(entry['GYT']))]
    self.df = pd.concat([self.df, pd.DataFrame.from_dict(entry)])
  
  def save_data(self) -> str:
    self.df.to_csv(path_or_buf=self.filename, index=False)
    return self.filename
      
  def run(self):
    if self.ser.in_waiting != 0:
      print("Message received")
      if self.ser.readline().decode().startswith("BGD"):
        print("Sensor data detected")
        self.receive_data_packet()
        describe_data(self.df.iloc[-400:])      
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
    filepath = serial.save_data()
    describe_data(filepath)
    serial.close()
    print("Comms closed")
          
        
    
