import pandas as pd, numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def import_data(filepath : str) -> pd.DataFrame:
  return pd.read_csv(filepath)

def get_sampling_rate(data : pd.DataFrame):
  max = data.groupby('message')['GYT'].max()
  min = data.groupby('message')['GYT'].min()
  size = data.groupby('message')['GYT'].size()
  print("Sampling rate")
  print(size / ((max - min) / 1000) )
  
  
def plot_data(df : pd.DataFrame):
  labels = ['ACZ', 'DIS']
  fig,axes = plt.subplots(nrows=len(labels), ncols=1)
  for ax in plt.gcf().axes:
    ax.cla()
  for (ind,label) in enumerate(labels):
    sns.scatterplot(data=df, x='GYT', y=label, hue='message', ax=axes[ind])
  plt.pause(0.1)
  
def describe_data(data : pd.DataFrame):
  get_sampling_rate(data)
  plot_data(data)
  
def smooth_data(data : pd.DataFrame):
  data['ACX'] = data['ACX'].rolling(window=2).mean()
  data['ACY'] = data['ACY'].rolling(window=2).mean()
  data['ACZ'] = data['ACZ'].rolling(window=2).mean()
  data['RTX'] = data['RTX'].rolling(window=2).mean()
  data['RTY'] = data['RTY'].rolling(window=2).mean()
  data['RTZ'] = data['RTZ'].rolling(window=2).mean()
  return data

def calculate_derivative(data : pd.DataFrame):
  data['ACX'] = np.gradient(data['ACX'])
  data['ACY'] = np.gradient(data['ACY'])
  data['ACZ'] = np.gradient(data['ACZ'])
  data['RTX'] = np.gradient(data['RTX'])
  data['RTY'] = np.gradient(data['RTY'])
  data['RTZ'] = np.gradient(data['RTZ'])
  return data

def detrend(data : pd.DataFrame):
  data['ACZ'] = data['ACZ'] - data['ACZ'].mean()
  data['DIS'] = data['DIS'] - data['DIS'].mean()
  dis_dev = data['DIS'].std()
  acc_dev = data['ACZ'].std()
  data['DIS'] = data['DIS']
  data['ACZ'] = data['ACZ']
  peaks = []
  for val in data['ACZ']:
    if (val > 3 * acc_dev and val > 2):
      peaks.append(1)
    elif val < -3 * acc_dev and val < -2:
      peaks.append(-1)
  print("Peaks:", peaks)
  if peaks.count(1) > 0 and peaks.count(-1) > 0:
    if peaks.index(1) > peaks.index(-1):
      print('Speedbump')
    else:
      print('Pothole')
  elif peaks.count(1) > 0:
    print('Speedbump')
  elif peaks.count(-1) > 0:
    print('Pothole')
  else:
    print('None')

  return data
  
  
if __name__ == "__main__":
  filepath = "PotholeData/09_06_2024_T18_12_59.csv"
  data = import_data(filepath)
  for i in data['message'].values.tolist():
    print(f"Msg #{i}")
    current = data[data['message'] == i]
    detrend(current)
  # describe_data(data)
  # print(data['ACZ'].std())

  
  
  
  