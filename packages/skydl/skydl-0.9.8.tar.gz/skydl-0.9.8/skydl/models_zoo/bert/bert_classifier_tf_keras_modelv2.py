# -*- coding: utf-8 -*-
import sys
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from skydl.models.train_phase_enum import TrainPhaseEnum
from skydl.models.tf_keras_modelv2 import TfKerasModelV2
from py_common_util.common.annotations import print_exec_time
from skydl.datasets.chinese_bert_classifier_dataset_builder import ChineseBertClassifierDatasetBuilder


class BertClassifierNerTfKerasModelV2(TfKerasModelV2):
    """bert分类模型"""
    def adjust_parse_args_value(self):
        super().adjust_parse_args_value()
        self.parser_args.data_path = sys.path[0] + '/../../datasets'
        self.parser_args.use_cuda = True
        self.parser_args.init_from_saver = True
        self.parser_args.fit_initial_epoch = 0
        self.parser_args.train_phase = TrainPhaseEnum.Train.value
        self.parser_args.model_version = '20200217011'
        self.parser_args.epochs = 3
        self.parser_args.batch_size = 32
        self.parser_args.log_interval = 1000

    @print_exec_time
    def load_data(self, *args, **kwargs):
        dataset_name = ChineseBertClassifierDatasetBuilder.camelcase_to_snakecase("ChineseBertClassifierDatasetBuilder")
        batched_datasets = ChineseBertClassifierDatasetBuilder.load_batched_datasets(dataset_name, config_name="plain_text")
        num_examples = ChineseBertClassifierDatasetBuilder.get_num_examples(dataset_name, tfds.Split.TRAIN)
        print(f"BertClassifierNerTfKerasModelV2 dataset num_examples={num_examples}")
        train_data = ChineseBertClassifierDatasetBuilder.load_batched_datasets(dataset_name,
                                                                      split=[tfds.Split.TRAIN],
                                                                      shuffle=1000,
                                                                      batch_size=self.parser_args.batch_size,
                                                                      epochs=1)
        validation_data = ChineseBertClassifierDatasetBuilder.load_batched_datasets(dataset_name,
                                                                      split=[tfds.Split.VALIDATION],
                                                                      shuffle=1000,
                                                                      batch_size=self.parser_args.batch_size,
                                                                      epochs=1)
        evaluate_data = ChineseBertClassifierDatasetBuilder.load_batched_datasets(dataset_name,
                                                                      split=[tfds.Split.TEST],
                                                                      shuffle=1000,
                                                                      batch_size=self.parser_args.batch_size,
                                                                      epochs=1)
        return train_data, validation_data, evaluate_data

    @print_exec_time
    def fit(self, *args, **kwargs):
        if not self.is_training_phase():
            return self
        loaded_dataset = kwargs.get("loaded_dataset")
        batched_train_dataset = loaded_dataset[0]
        batched_evaluate_dataset = loaded_dataset[2]
        self.model.get_proxy().fit(batched_train_dataset,
                                   epochs=self.parser_args.epochs,
                                   initial_epoch=self.parser_args.fit_initial_epoch,
                                   callbacks=self._fit_callbacks())
        self.model.get_proxy().summary()
        # evaluate model
        self.evaluate(batched_evaluate_dataset)
        # predict model
        predict_result = self.model.get_proxy().predict(batched_evaluate_dataset)
        self.log.info(f"fit#predict_result={predict_result}")
        # moreover, save mode to h5 file
        self.model.get_proxy().save(self.get_model_saved_dir() + "/saved_model.h5")
        self.log.info(f"tf.keras trained model was already saved to : {self.get_model_saved_dir()}/saved_model.h5")
        # change to inference phase
        self.parser_args.train_phase = TrainPhaseEnum.Inference.value
        return self

    def evaluate(self, *args, **kwargs):
        data = args[0]
        if data:
            self.model.get_proxy().evaluate(data)
            self.model.get_proxy().summary()
            # change to evaluate phase
            self.parser_args.train_phase = TrainPhaseEnum.Evaluate.value
        return self

    @print_exec_time
    def predict_from_load_weights(self, *args, **kwargs):
        """python版的预测接口，返回预测结果"""
        if not self.is_inference_phase():
            return None
        # # restore weights from saved model file
        # model = tf.keras.models.load_model(self.get_model_saved_dir() + "/saved_model.h5")
        # self.log.info(f"already called load_model from: {self.get_model_saved_dir()}/saved_model.h5")
        # restore weights from latest checkpoint
        self.log.info(f"predict_from_load_weights#get_model_checkpoint_dir={self.get_model_checkpoint_dir()}")
        latest_checkpoint = tf.train.latest_checkpoint(self.get_model_checkpoint_dir())
        if latest_checkpoint:
            self.model.get_proxy().load_weights(latest_checkpoint)
            self.log.info(f"already called load_weights from: {latest_checkpoint}")
        # predict sample
        batch_size = 100
        max_seq_length = 128
        inputs = {
            "input_ids": np.reshape(np.array([1001] * batch_size * max_seq_length), (batch_size, max_seq_length)),
            "input_mask": np.reshape(np.array([1] * batch_size * max_seq_length), (batch_size, max_seq_length)),
            "segment_ids": np.reshape(np.array([200] * batch_size * max_seq_length), (batch_size, max_seq_length))
        }
        # predictions = self.model.get_proxy().predict([np.array([1001]*128), np.array([1]*128), np.array([1001]*128)])  # XXX
        ########################
        dataset_name = ChineseBertClassifierDatasetBuilder.camelcase_to_snakecase("ChineseBertClassifierDatasetBuilder")
        valid_data = ChineseBertClassifierDatasetBuilder.load_batched_datasets(dataset_name,
                                                                      split=[tfds.Split.TRAIN],
                                                                      shuffle=1000,
                                                                      batch_size=self.parser_args.batch_size,
                                                                      epochs=1)
        predictions = self.model.get_proxy().predict(valid_data.take(1))
        # predictions = np.array([a[0] for a in predictions])
        print(f"predictions={predictions}")
