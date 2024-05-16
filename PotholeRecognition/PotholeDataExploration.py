import pandas as pd, numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

fig,axes = plt.subplots(nrows=7, ncols=1)

def import_data(filepath : str) -> pd.DataFrame:
  return pd.read_csv(filepath)

def get_sampling_rate(data : pd.DataFrame):
  max = data.groupby('message')['GYT'].max()
  min = data.groupby('message')['GYT'].min()
  size = data.groupby('message')['GYT'].size()
  print("Sampling rate")
  print(size / ((max - min) / 1000) )
  
  
def plot_data(df : pd.DataFrame):
  labels = ['DIS', 'ACX', 'ACY', 'ACZ', 'RTX', 'RTY', 'RTZ']
  for ax in plt.gcf().axes:
    ax.cla()
  for (ind,label) in enumerate(labels):
    sns.scatterplot(data=df, x='GYT', y=label, hue='message', ax=axes[ind])
  plt.pause(0.1)
  
def describe_data(data : pd.DataFrame):
  get_sampling_rate(data)
  plot_data(data)
  
if __name__ == "__main__":
  filepath = "PotholeData/09_05_2024_T14_16_40.csv"
  data = import_data(filepath)
  describe_data(data)
  
  