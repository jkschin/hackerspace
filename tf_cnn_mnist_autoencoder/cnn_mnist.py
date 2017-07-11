
#  Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Convolutional Neural Network Estimator for MNIST, built with tf.layers."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2
import numpy as np
import tensorflow as tf

from tensorflow.contrib import learn
from tensorflow.contrib.learn.python.learn.estimators import model_fn as model_fn_lib

tf.logging.set_verbosity(tf.logging.INFO)


def cnn_model_fn(features, labels, mode):
  with tf.get_default_graph().as_default():
    input_layer = tf.reshape(features, [-1, 28, 28, 1])
    conv1 = tf.layers.conv2d(
        inputs=input_layer,
        filters=32,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)
    conv2 = tf.layers.conv2d(
        inputs=conv1,
        filters=64,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)
    conv3 = tf.layers.conv2d(
        inputs=conv2,
        filters=128,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)
    dropout = tf.layers.dropout(
        inputs=conv3, rate=0.4, training=mode == learn.ModeKeys.TRAIN)
    conv4 = tf.layers.conv2d(
        inputs=dropout,
        filters=1,
        kernel_size=[5, 5],
        padding="same",
        activation=None)
    logits = conv4
  loss = None
  train_op = None

  # Calculate Loss (for both TRAIN and EVAL modes)
  if mode != learn.ModeKeys.INFER:
    labels = tf.reshape(labels, [-1, 28, 28, 1])
    loss = tf.losses.mean_squared_error(
        labels=labels,
        predictions=logits)

  # Configure the Training Op (for TRAIN mode)
  if mode == learn.ModeKeys.TRAIN:
    train_op = tf.contrib.layers.optimize_loss(
        loss=loss,
        global_step=tf.contrib.framework.get_global_step(),
        learning_rate=0.001,
        optimizer="SGD")

  # Generate Predictions
  predictions = {
      "image": logits
      # "classes": tf.argmax(
      #     input=logits, axis=1),
      # "probabilities": tf.nn.softmax(
      #     logits, name="softmax_tensor")
  }

  # Return a ModelFnOps object
  return model_fn_lib.ModelFnOps(
      mode=mode, predictions=predictions, loss=loss, train_op=train_op)


def main(unused_argv):
  # Load training and eval data
  mnist = learn.datasets.load_dataset("mnist")
  train_data = mnist.train.images  # Returns np.array
  train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
  eval_data = mnist.test.images  # Returns np.array
  eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

  # Create the Estimator
  mnist_classifier = learn.Estimator(
      model_fn=cnn_model_fn, model_dir="/tmp/mnist_convnet_model")

  # Set up logging for predictions
  # Log the values in the "Softmax" tensor with label "probabilities"
  # tensors_to_log = {"probabilities": "softmax_tensor"}
  # logging_hook = tf.train.LoggingTensorHook(
  #     tensors=tensors_to_log, every_n_iter=50)

  # Train the model
  # mnist_classifier.fit(
  #     x=train_data,
  #     y=train_data,
  #     batch_size=100,
  #     steps=20000)
      # monitors=[logging_hook])

  sample = eval_data[1]
  predictions = list(mnist_classifier.predict(
      x=sample,
      as_iterable=True))
  predictions = predictions[0]["image"]

  orig = np.reshape(sample, (28, 28)) * 255.0
  pred = np.reshape(predictions, (28, 28)) * 255.0

  cv2.imwrite('orig.png', orig)
  cv2.imwrite('pred.png', pred)

  # Configure the accuracy metric for evaluation
  # metrics = {
  #     "accuracy":
  #         learn.MetricSpec(
  #             metric_fn=tf.metrics.accuracy, prediction_key="classes"),
  # }

  # Evaluate the model and print results
  # eval_results = mnist_classifier.evaluate(
  #     x=eval_data, y=eval_labels, metrics=metrics)
  # print(eval_results)


if __name__ == "__main__":
  tf.app.run()
