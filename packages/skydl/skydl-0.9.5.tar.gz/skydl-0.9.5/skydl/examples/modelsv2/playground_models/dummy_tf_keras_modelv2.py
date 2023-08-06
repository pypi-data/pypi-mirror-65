# -*- coding: utf-8 -*-
import sys
import numpy as np
from skydl.datasets.movielens_dataset_builder import MovieLensDatasetBuilder
from skydl.models.tf_keras_modelv2 import TfKerasModelV2
from tensorflow.python import keras  # 或from tensorflow import keras
from skydl.models.train_phase_enum import TrainPhaseEnum


class DummyTfKerasModelV2(TfKerasModelV2):

    def adjust_parse_args_value(self):
        super().adjust_parse_args_value()
        self.parser_args.data_path = sys.path[0] + '/../../dataset'
        self.parser_args.use_cuda = True
        self.parser_args.init_from_saver = True
        self.parser_args.train_phase = TrainPhaseEnum.Train.value
        self.parser_args.model_version = '1'
        self.parser_args.epochs = 1
        self.parser_args.batch_size = 128
        self.parser_args.log_interval = 1000

    def build_network(self):
        return super().build_network()

    def compile(self, loss=keras.losses.sparse_categorical_crossentropy, optimizer=keras.optimizers.Adam(), metrics=["accuracy"]):
        return super().compile(loss, optimizer, metrics)

    def fit(self, *args, **kwargs):
        print(self.is_training_phase())
        if not self.is_training_phase():
            return self
        train_dataset, validation_dataset, test_dataset, np_user_ids, np_item_ids, np_labels = self.load_data()
        user_feature_column = MovieLensDatasetBuilder.build_numeric_feature_columns(["user_id"])
        item_feature_column = MovieLensDatasetBuilder.build_numeric_feature_columns(["item_id"])
        total_items = len(np.unique(np_item_ids))
        total_users = len(np.unique(np_user_ids))

        # creating user embedding path
        user_input = keras.Input(shape=[1], name="User-Input")
        user_embedding = keras.layers.Embedding(total_users, 10, name="User-Embedding")(user_input)
        user_vec = keras.layers.Flatten(name="Flatten-Users")(user_embedding)

        # creating book embedding path
        book_input = keras.Input(shape=[1], name="Book-Input")
        book_embedding = keras.layers.Embedding(total_items, 10, name="Book-Embedding")(book_input)
        book_vec = keras.layers.Flatten(name="Flatten-Books")(book_embedding)

        # performing dot product and creating model
        prod = keras.layers.Dot(name="Dot-Product", axes=1)([book_vec, user_vec])
        model = keras.Model([user_input, book_input], prod)
        model.compile('adam', 'mean_squared_error', ["accuracy"])
        model.fit([np_user_ids] + [np_item_ids], np_labels)
        model.summary()
        return self

    def evaluate(self, *args, **kwargs):
        return super().evaluate(*args, **kwargs)

    def serving(self, *args, **kwargs):
        return super().serving(*args, **kwargs)

    def predict(self, *args, **kwargs):
        return super().predict(*args, **kwargs)
