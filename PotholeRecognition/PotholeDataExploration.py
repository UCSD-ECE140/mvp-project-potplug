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
  
def describe_data(data : pd.DataFrame):
  data.describe()
  
  
def plot_data(df : pd.DataFrame):
  fig, axes = plt.subplots(nrows=7, ncols=1)
  sns.lineplot(data=df, x='DST', y ='DIS', hue='message', ax=axes[0])
  labels = ['ACX', 'ACY', 'ACZ', 'RTX', 'RTY', 'RTZ']
  for (ind,label) in enumerate(labels):
    sns.lineplot(data=df, x='GYT', y=label, hue='message', ax=axes[1+ind])
  plt.show()
  
def describe_data(filepata = None, data=None):
  if filepath != None:
    data = import_data(filepath)
  get_sampling_rate(data)
  plot_data(data)
  
if __name__ == "__main__":
  filepath = "PotholeData/09_05_2024_T14_16_40.csv"
  describe_data(filepath)
  
  