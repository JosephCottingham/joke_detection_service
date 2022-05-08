import tensorflow as tf

import tfx
from tfx.components.trainer.executor import TrainerFnArgs

from tfx_bsl.public import tfxio

import tensorflow_transform as tft
from tensorflow_transform.tf_metadata import schema_utils

from typing import List
from absl import logging

from model import build_model

BATCH_SIZE = 64
STEPS_PER_EPOCH = 250

TRAIN_BATCH_SIZE = 20
EVAL_BATCH_SIZE = 10

from features import FEATURE_KEYS, LABEL_KEY

# Since we're not generating or creating a schema, we will instead create
# a feature spec.  Since there are a fairly small number of features this is
# manageable for this dataset.
FEATURE_SPEC = {
    **{
        feature: tf.io.FixedLenFeature(shape=(), dtype=tf.string)
           for feature in FEATURE_KEYS
       },
    LABEL_KEY: tf.io.FixedLenFeature(shape=[1], dtype=tf.int64)
}


SCHEMA = schema_utils.schema_from_feature_spec(FEATURE_SPEC)

def _input_fn(file_pattern: List[str],
              data_accessor,
              schema,
              batch_size: int = 200) -> tf.data.Dataset:
  """Generates features and label for training.

  Args:
    file_pattern: List of paths or patterns of input tfrecord files.
    data_accessor: DataAccessor for converting input to RecordBatch.
    schema: schema of the input data.
    batch_size: representing the number of consecutive elements of returned
      dataset to combine in a single batch

  Returns:
    A dataset that contains (features, indices) tuple where features is a
      dictionary of Tensors, and indices is a single Tensor of label indices.
  """
  return data_accessor.tf_dataset_factory(
      file_pattern,
      tfxio.TensorFlowDatasetOptions(batch_size=batch_size, label_key=LABEL_KEY),
      schema=SCHEMA
      ).repeat()

def run_fn(training_args: TrainerFnArgs):
    train_steps = training_args.train_steps
    eval_steps = training_args.eval_steps

    train_dataset = _input_fn(
        training_args.train_files,
        training_args.data_accessor,
        SCHEMA,
        batch_size=TRAIN_BATCH_SIZE)
    eval_dataset = _input_fn(
        training_args.eval_files,
        training_args.data_accessor,
        SCHEMA,
        batch_size=EVAL_BATCH_SIZE)
    
    model = build_model()
    model.fit(
        train_dataset,
        steps_per_epoch=training_args.train_steps,
        validation_data=eval_dataset,
        validation_steps=training_args.eval_steps
    )

    # The result of the training should be saved in `fn_args.serving_model_dir`
    # directory.
    model.save(training_args.serving_model_dir, save_format='tf')