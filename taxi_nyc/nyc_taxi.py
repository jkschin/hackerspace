import tensorflow as tf
tf.logging.set_verbosity(tf.logging.INFO)

BATCH_SIZE = 256
CSV_PATH = '/home/jkschin/Downloads/2017_Green_Taxi_Trip_Data.csv'
COLUMN_NAMES = ['VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime',
    'store_and_fwd_flag', 'RatecodeID', 'PULocationID', 'DOLocationID',
    'passenger_count', 'trip_distance', 'fare_amount', 'extra', 'mta_tax',
    'tip_amount', 'tolls_amount', 'ehail_fee', 'improvement_surcharge',
    'total_amount', 'payment_type', 'trip_type']

RECORD_DEFAULTS = [ [0], ['NA'], ['NA'], ['NA'], [0], [0], [0], [0.0],
    [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0], [0]]

def _parse_line(line):
  fields = tf.decode_csv(line, record_defaults=RECORD_DEFAULTS)
  features = dict(zip(COLUMN_NAMES, fields))
  features['PULocationID'] -= 1
  features['DOLocationID'] -= 1
  label = features.pop('tip_amount')
  return features, label

def csv_input_fn(csv_path, batch_size):
  # Skip the headers
  dataset = tf.data.TextLineDataset(csv_path).skip(1)
  dataset = dataset.map(_parse_line)
  dataset = dataset.shuffle(1000).repeat().batch(batch_size)
  return dataset

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
    tf.feature_column.indicator_column(vendor_id),
    tf.feature_column.indicator_column(pu_location_id),
    tf.feature_column.indicator_column(do_location_id),
    tf.feature_column.numeric_column('passenger_count'),
    tf.feature_column.numeric_column('trip_distance'),
    tf.feature_column.numeric_column('fare_amount'),
    tf.feature_column.numeric_column('extra'),
    tf.feature_column.numeric_column('mta_tax'),
    tf.feature_column.numeric_column('tolls_amount'),
    tf.feature_column.numeric_column('improvement_surcharge'),
    tf.feature_column.numeric_column('total_amount'),
    tf.feature_column.indicator_column(payment_type),
    tf.feature_column.indicator_column(trip_type)
    ]
est = tf.estimator.DNNRegressor(
    feature_columns=feature_columns,
    hidden_units=[100, 100])
est.train(
    steps=1000,
    input_fn=lambda: csv_input_fn(CSV_PATH, BATCH_SIZE))

# dataset = csv_input_fn(CSV_PATH, BATCH_SIZE)
# iterator = dataset.make_initializable_iterator()
# next_element = iterator.get_next()
# sess = tf.Session()
# sess.run(tf.global_variables_initializer())
# sess.run(iterator.initializer)
# for _ in xrange(100):
#   a, b = sess.run(next_element)
#   print b
#   break


