# -*- coding: utf-8 -*-
import numpy as np
import tensorflow_datasets as tfds
from skydl.models.train_phase_enum import TrainPhaseEnum
from skydl.datasets.movielens_dataset_builder import MovieLensDatasetBuilder
from skydl.models_zoo.cv.minist_tf_keras_modelv2_main import training_mnist_tf_keras_model
from skydl.examples.modelsv2.playground_models.dummy_tf_keras_modelv2 import DummyTfKerasModelV2
from skydl.models_zoo.recommendation.wide_and_deep_tf_keras_modelv2_main import training_wide_and_deep_keras_model


def run_example_0():
    def load_data_fn(parser_args):
        print(f"load_data_fn......{parser_args}")
        dataset_name = MovieLensDatasetBuilder.camelcase_to_snakecase("MovieLensDatasetBuilder")
        num_examples = MovieLensDatasetBuilder.get_num_examples(dataset_name)
        full_datasets = MovieLensDatasetBuilder.load_batched_datasets(dataset_name,
                                                                      split=[tfds.Split.TRAIN],
                                                                      batch_size=128,
                                                                      epochs=1)
        train_data, validation_data, evaluate_data = MovieLensDatasetBuilder.split_full_datasets(full_datasets,
                                                                                                      num_examples=MovieLensDatasetBuilder.get_total_num_batch(
                                                                                                          num_examples,
                                                                                                          128),
                                                                                                      train_size=0.7,
                                                                                                      validation_size=0,
                                                                                                      test_size=0.2)
        np_user_ids = np.array([])
        np_item_ids = np.array([])
        np_labels = np.array([])
        if parser_args.train_phase == TrainPhaseEnum.Train.value:
            # get 2 batched test_dataset: i.e. 128 * 3
            stat_dataset = evaluate_data.take(3)
        else:
            # get train_dataset
            stat_dataset = train_data
        for features, labels in MovieLensDatasetBuilder.read_batched_datasets(stat_dataset):
            np_user_ids = np.append(np_user_ids, features['user_id'])
            np_item_ids = np.append(np_item_ids, features['item_id'])
            np_labels = np.append(np_labels, labels)
        return train_data, validation_data, evaluate_data, np_user_ids, np_item_ids, np_labels
    # kick of training
    DummyTfKerasModelV2("TfKerasModelV2-0",
    ).set_load_data_fn(
        load_data_fn
    ).compile(
    ).fit(
    )


def run_example_1():
    training_wide_and_deep_keras_model()


def run_mnist():
    training_mnist_tf_keras_model()


if __name__ == '__main__':
    # run_example_0()
    # run_example_1()
    run_mnist()

