import tensorflow as tf
import tensorflow.feature_column as fc
import os
import sys
import matplotlib.pyplot as plt
import pandas
import functools

tf.logging.set_verbosity(tf.logging.INFO)

train_file = 'train.csv'
test_file = 'test.csv'

train_df = pandas.read_csv(train_file)
test_df = pandas.read_csv(test_file)

def easy_input_function(df, label_key, num_epochs, shuffle, batch_size):
  label = df[label_key]
  ds = tf.data.Dataset.from_tensor_slices((dict(df),label))

  if shuffle:
    ds = ds.shuffle(10000)

  ds = ds.batch(batch_size).repeat(num_epochs)

  return ds

def custom_numeric_column(key):
  col = tf.feature_column.numeric_column(key,
      normalizer_fn=lambda x: (x - STATS[key]['mean']) / STATS[key]['stddev'])
  return col

def compute_statistics(df):
  # TODO: Transfer this cast and relevant code here to the cleaning step.
  df['passenger_count'] = df['passenger_count'].astype('float64')
  statistics = {}
  for key in df.keys():
    if df[key].dtype == 'float64':
      statistics[key] = {}
      statistics[key]['mean'] = df[key].mean()
      statistics[key]['stddev'] = df[key].std()
      print key, statistics[key]['mean'], statistics[key]['stddev']
  return statistics

STATS = compute_statistics(train_df)

train_inpf = functools.partial(easy_input_function, train_df, 'tip',
    num_epochs=2, shuffle=True, batch_size=64)
test_inpf = functools.partial(easy_input_function, test_df, 'tip', num_epochs=1,
    shuffle=False, batch_size=64)
pu_location_id = tf.feature_column.categorical_column_with_identity(
    key='PULocationID',
    num_buckets=265
)
do_location_id = tf.feature_column.categorical_column_with_identity(
    key='DOLocationID',
    num_buckets=265
)
day_of_week = tf.feature_column.categorical_column_with_identity(
    key='day_of_week',
    num_buckets=7
)
weekend = tf.feature_column.categorical_column_with_identity(
    key='weekend',
    num_buckets=2
)
categorical_columns = [
  fc.indicator_column(pu_location_id),
  fc.indicator_column(do_location_id),
  fc.indicator_column(day_of_week),
  fc.indicator_column(weekend)
  ]
numeric_columns = [
  custom_numeric_column('passenger_count'),
  custom_numeric_column('trip_distance'),
  custom_numeric_column('fare_amount'),
  custom_numeric_column('extra'),
  custom_numeric_column('mta_tax'),
  custom_numeric_column('tolls_amount'),
  custom_numeric_column('improvement_surcharge'),
  custom_numeric_column('total_amount'),
  custom_numeric_column('duration'),
  custom_numeric_column('speed')
  ]
feature_columns = numeric_columns

classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,
    n_classes=2,
    hidden_units=[2048,2048,1024,512,256,128,64],
    batch_norm=True,
    activation_fn=tf.nn.leaky_relu,
    optimizer=tf.train.AdamOptimizer(0.0005)
    )
classifier.train(train_inpf)
result = classifier.evaluate(test_inpf)

print(result)

# ds = easy_input_function(train_df, 'tip', 10, True, 32)

# for feature_batch, label_batch in ds.take(1):
#   print('Some feature keys:', list(feature_batch.keys())[:5])
#   print()
#   print('A batch of Tips :', feature_batch['tip_amount'])
#   print()
#   print('A batch of Labels:', label_batch )

# fc.input_layer(feature_batch, ['tip_amount']).numpy()





