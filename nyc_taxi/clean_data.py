import pandas as pd
import numpy as np

TRAIN_PATH = '/home/jkschin/code/hackerspace/nyc_taxi/train_all_payments.csv'
TEST_PATH = '/home/jkschin/code/hackerspace/nyc_taxi/test_all_payments.csv'
INPUT_PATH = '/home/jkschin/code/hackerspace/nyc_taxi/original.csv'

def label_weekend(row):
  if row['day_of_week'] in [0, 1, 2, 3, 4]:
    return 0
  else:
    return 1

def label_tip(row):
  if row['tip_amount'] > 0:
    return 1
  else:
    return 0

def clean_passenger_count(row):
  if row['passenger_count'] == 0:
    return 1
  else:
    return row['passenger_count']

def main():
  print "Reading data."
  df = pd.read_csv(INPUT_PATH)
  total_rows_before = len(df.index)
  print "Total rows before filtering: %d" %(total_rows_before)

  print "Casting columns."
  df['passenger_count'] = df['passenger_count'].astype('float64')

  print "Filtering data."
  df = df[df['RatecodeID'] != 99]
  df = df[df['fare_amount'] >= 0]
  df = df[df['extra'] >= 0]
  df = df[df['mta_tax'] >= 0]
  df = df[df['tip_amount'] >= 0]
  df = df[df['tolls_amount'] >= 0]
  df = df[df['improvement_surcharge'] >= 0]
  df = df[df['total_amount'] >= 0]
  # Only keep credit card trips.
  # df = df[df['payment_type'] == 1]
  total_rows_after = len(df.index)
  total_rows_diff = total_rows_before - total_rows_after
  print "Total rows after filtering: %d" %(total_rows_after)
  print "Filtered rows: %d" %(total_rows_diff)

  print "Transforming data."
  # It's necessary to include the format to speed up the transformation.
  print "Transforming lpep_pickup_datetime."
  df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'],
      format='%m/%d/%Y %I:%M:%S %p')
  print "Transforming lpep_dropoff_datetime."
  df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'],
      format='%m/%d/%Y %I:%M:%S %p')
  print "Transforming duration."
  df['duration'] = df['lpep_dropoff_datetime'] - df['lpep_pickup_datetime']
  df['duration'] = df['duration'] / np.timedelta64(1, 's')
  # Removes 1252 Rows
  df = df[df['duration'] > 0]
  # Just use pickup datetime and ignore dropoff.
  print "Transforming day_of_week."
  df['day_of_week'] = df['lpep_pickup_datetime'].dt.dayofweek
  print "Transforming weekend."
  df['weekend'] = df.apply(lambda row: label_weekend(row), axis=1)
  print "Transforming speed."
  df['speed'] = df['trip_distance'] / df['duration'] * 3600
  print "Transforming tip."
  df['tip'] = df.apply(lambda row: label_tip(row), axis=1)
  print "Transforming passenger_count."
  df['passenger_count'] = df.apply(lambda row: clean_passenger_count(row), axis=1)
  print "Transforming PULocationID."
  df['PULocationID'] = df['PULocationID'] - 1
  print "Transforming DOLocationID."
  df['DOLocationID'] = df['DOLocationID'] - 1

  print "Writing training data."
  train = df.sample(frac=0.8, random_state=200)
  train.to_csv(TRAIN_PATH, index=False)
  print "Writing testing data."
  test = df.drop(train.index)
  test.to_csv(TEST_PATH, index=False)

def adhoc():
  train = pd.read_csv(TRAIN_PATH)
  test = pd.read_csv(TEST_PATH)
  train = train[train['duration'] > 0]
  test = test[test['duration'] > 0]
  train.to_csv(TRAIN_PATH, index=False)
  test.to_csv(TEST_PATH, index=False)

if __name__ == '__main__':
  main()
