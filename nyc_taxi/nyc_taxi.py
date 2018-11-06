import pandas as pd
import tensorflow as tf
import pickle
tf.logging.set_verbosity(tf.logging.INFO)

BATCH_SIZE = 256
TRAIN_PATH = '/home/jkschin/code/hackerspace/nyc_taxi/train.csv'
TEST_PATH = '/home/jkschin/code/hackerspace/nyc_taxi/test.csv'
COLUMN_NAMES = ['VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime',
    'store_and_fwd_flag', 'RatecodeID', 'PULocationID', 'DOLocationID',
    'passenger_count', 'trip_distance', 'fare_amount', 'extra', 'mta_tax',
    'tip_amount', 'tolls_amount', 'ehail_fee', 'improvement_surcharge',
    'total_amount', 'payment_type', 'trip_type', 'duration', 'day_of_week',
    'weekend', 'speed', 'tip']

RECORD_DEFAULTS = [ [0], ['NA'], ['NA'], ['NA'], [0], [0], [0], [0.0],
    [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0], [0.0],
    [0.0], [0], [0], [0.0], [0]]
COMPUTE_STATS = False

def compute_statistics():
  df = pd.read_csv(TRAIN_PATH)
  # TODO: Transfer this cast and relevant code here to the cleaning step.
  df['passenger_count'] = df['passenger_count'].astype('float64')
  statistics = {}
  for key in df.keys():
    if df[key].dtype == 'float64':
      print key
      statistics[key] = {}
      statistics[key]['mean'] = df[key].mean()
      statistics[key]['stddev'] = df[key].std()

# Only need to compute once and dump it in pickle.
if COMPUTE_STATS:
  STATS = compute_statistics()
  with open('stats.pickle', 'wb') as f:
    pickle.dump(STATS, f)
else:
  with open('stats.pickle', 'rb') as f:
    STATS = pickle.load(f)

def _parse_line(line):
  fields = tf.decode_csv(line, record_defaults=RECORD_DEFAULTS)
  features = dict(zip(COLUMN_NAMES, fields))
  # TODO: Transfer this into the cleaning step.
  features['PULocationID'] -= 1
  features['DOLocationID'] -= 1
  # label = features.pop('tip_amount')
  # label = (label - STATS['tip_amount']['mean']) / STATS['tip_amount']['stddev']
  label = features.pop('tip')
  return features, label

def csv_input_fn(csv_path, batch_size):
  # Skip the headers
  dataset = tf.data.TextLineDataset(csv_path).skip(1)
  dataset = dataset.map(_parse_line)
  dataset = dataset.shuffle(100000).repeat().batch(batch_size)
  return dataset

def eval_input_fn(csv_path):
  dataset = tf.data.TextLineDataset(csv_path).skip(1)
  dataset = dataset.map(_parse_line)
  return dataset

def custom_numeric_column(key):
  col = tf.feature_column.numeric_column(key,
      normalizer_fn=lambda x: (x - STATS[key]['mean']) / STATS[key]['stddev'])
  return col

vendor_id = tf.feature_column.categorical_column_with_vocabulary_list(
    key='VendorID',
    vocabulary_list=(1, 2)
)
pu_location_id = tf.feature_column.categorical_column_with_identity(
    key='PULocationID',
    num_buckets=265
)
do_location_id = tf.feature_column.categorical_column_with_identity(
    key='DOLocationID',
    num_buckets=265
)
payment_type = tf.feature_column.categorical_column_with_vocabulary_list(
    key='payment_type',
    vocabulary_list=(1, 2, 3, 4, 5)
)
trip_type = tf.feature_column.categorical_column_with_vocabulary_list(
    key='trip_type',
    vocabulary_list=(1, 2),
    num_oov_buckets=1
)
feature_columns = [
    # tf.feature_column.indicator_column(vendor_id),
    # tf.feature_column.indicator_column(pu_location_id),
    # tf.feature_column.indicator_column(do_location_id),
    custom_numeric_column('passenger_count'),
    custom_numeric_column('trip_distance'),
    custom_numeric_column('fare_amount'),
    custom_numeric_column('extra'),
    custom_numeric_column('mta_tax'),
    custom_numeric_column('tolls_amount'),
    custom_numeric_column('improvement_surcharge'),
    custom_numeric_column('total_amount')
    # tf.feature_column.indicator_column(payment_type),
    # tf.feature_column.indicator_column(trip_type)
    ]
# dataset = tf.data.TextLineDataset(TRAIN_PATH).skip(1)
# dataset = dataset.map(_parse_line)
# dataset = dataset.shuffle(100000).repeat().batch(BATCH_SIZE)
# features = tf.parse_example(dataset,
#     features=tf.feature_column.make_parse_example_spec(feature_columns))
# layers = [tf.feature_column.input_layer(features, feature_columns)]
# layers.append(tf.layers.dense(layers[-1], 2048))
# layers.append(tf.layers.dense(layers[-1], 1))
# print layers
est = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,
    n_classes=2,
    hidden_units=[2048, 1024, 512, 256, 128, 64],
    batch_norm=True,
    activation_fn=tf.nn.relu,
    optimizer=lambda: tf.train.AdamOptimizer(
      learning_rate=0.001
      ))
est.train(
    steps=200,
    input_fn=lambda: csv_input_fn(TRAIN_PATH, BATCH_SIZE))
# pred = est.predict(input_fn=eval_input_fn(TEST_PATH),
#     yield_single_examples=False)
pred = est.evaluate(
    input_fn=lambda: eval_input_fn(TEST_PATH))

