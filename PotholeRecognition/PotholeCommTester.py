import serial
import pandas as pd
import numpy as np
from IPython.display import display
from datetime import datetime
from PotholeDataExploration import describe_data

class SerialHandler():
    ser = None
    df: pd.DataFrame
    msg_count: int
    filename: str
    
    bluetooth = "COM11"
    
    def __init__(self, _df: pd.DataFrame = None) -> None:
        try:
            self.ser = serial.Serial(port=self.bluetooth, baudrate=115200)
        except serial.SerialException as e:
            print(f"Failed to open serial port {self.bluetooth}: {e}")
            self.ser = None  # Ensure ser is None if connection fails

        self.df = pd.DataFrame() if _df is None else _df
        self.msg_count = 0
        self.filename = f"PotholeData/{datetime.now().strftime('%d_%m_%Y_T%H_%M_%S')}.csv"

    def receive_data_packet(self):
        if self.ser:
            message = self.ser.read_until(b"END")
            message = message.decode()
            self.parse_data_packet(message)
            self.msg_count += 1

    def parse_data_packet(self, message: str):
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
        if self.ser and self.ser.in_waiting != 0:
            print("Message received")
            message = self.ser.read_until().decode()
            print(message)
            if message.startswith('BGD'):
                print("Sensor data detected")
                self.receive_data_packet()
                describe_data(self.df.iloc[-400:])      

    def close(self):
        if self.ser:
            self.ser.close()

if __name__ == '__main__':
    serial_handler = None
    try:
        serial_handler = SerialHandler()
        if serial_handler.ser:
            print('Setup done')
            prev_count = 0
            while True:
                serial_handler.run()
                if serial_handler.msg_count != prev_count:
                    display(serial_handler.df)
                    prev_count = serial_handler.msg_count
        else:
            print("Serial connection could not be established.")
    finally:
        if serial_handler and serial_handler.ser:
            filepath = serial_handler.save_data()
            serial_handler.close()
            print("Comms closed")
