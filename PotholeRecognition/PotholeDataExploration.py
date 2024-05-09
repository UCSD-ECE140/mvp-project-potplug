import pandas as pd, numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def import_data(filepath : str) -> pd.DataFrame:
  return pd.read_csv(filepath)

def get_sampling_rate(data : pd.DataFrame):
  max = data.groupby('message')['DST'].max()
  min = data.groupby('message')['DST'].min()
  size = data.groupby('message')['DST'].size()
  print("Sampling rate")
  print(size / ((max - min) / 1000) )
  
def show_distance(df : pd.DataFrame):
  sns.lineplot(data=df, x='DST', y ='DIS', hue='message')
  plt.show()
  
def describe(filepath):
  data = import_data(filepath)
  get_sampling_rate(data)
  show_distance(data)
  
if __name__ == "__main__":
  filepath = "PotholeData/09_05_2024_T14_16_40.csv"
  describe(filepath)
  
  