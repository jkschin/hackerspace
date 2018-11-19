# import csv
import pandas as pd

# df = pd.read_csv('/home/jkschin/Downloads/2017_Green_Taxi_Trip_Data.csv')

# with open('/home/jkschin/Downloads/2017_Green_Taxi_Trip_Data.csv', 'rb') as f:
#   reader = csv.reader(f)
#   data = list(reader)

def compute_statistics():
  df = pd.read_csv('/home/jkschin/Downloads/2017_Green_Taxi_Trip_Data.csv')
  df['passenger_count'] = df['passenger_count'].astype('float64')
  statistics = {}
  for key in df.keys():
    if df[key].dtype == 'float64':
      print key
      statistics[key] = {}
      statistics[key]['mean'] = df[key].mean()
      statistics[key]['stddev'] = df[key].std()
  return statistics

dic = compute_statistics()
