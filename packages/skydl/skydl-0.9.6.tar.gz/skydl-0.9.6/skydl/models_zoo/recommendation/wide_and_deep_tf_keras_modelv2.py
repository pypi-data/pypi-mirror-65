# -*- coding: utf-8 -*-
import sys
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from skydl.models.train_phase_enum import TrainPhaseEnum
from skydl.models.tf_keras_modelv2 import TfKerasModelV2
from py_common_util.common.annotations import print_exec_time
from skydl.datasets.recommend_dataset_builder import RecommendDatasetBuilder


class WideAndDeepTfKerasModelV2(TfKerasModelV2):
    """
    资讯智能推荐系统中用于精排序模型实现
    """
    def adjust_parse_args_value(self):
        super().adjust_parse_args_value()
        self.parser_args.data_path = sys.path[0] + '/../../datasets'
        self.parser_args.use_cuda = True
        self.parser_args.init_from_saver = True
        self.parser_args.fit_initial_epoch = 0
        self.parser_args.train_phase = TrainPhaseEnum.Train.value
        self.parser_args.model_version = '20191108001'
        self.parser_args.epochs = 5
        self.parser_args.batch_size = 512
        self.parser_args.log_interval = 1000

    @print_exec_time
    def load_data(self, *args, **kwargs):
        super().load_data(*args, **kwargs)
        dataset_name = RecommendDatasetBuilder.camelcase_to_snakecase("RecommendDatasetBuilder")
        num_examples = RecommendDatasetBuilder.get_num_examples(dataset_name)
        full_datasets = RecommendDatasetBuilder.load_batched_datasets(dataset_name,
                                                                      split=[tfds.Split.TRAIN],
                                                                      shuffle=0,
                                                                      batch_size=self.parser_args.batch_size,
                                                                      epochs=1)
        train_data, \
        validation_data, \
            evaluate_data = RecommendDatasetBuilder.split_full_datasets(full_datasets,
                                                                   num_examples=RecommendDatasetBuilder.get_total_num_batch(num_examples, self.parser_args.batch_size),
                                                                   train_size=0.7,
                                                                   validation_size=0.1,
                                                                   test_size=0.2)
        # # 获取index_tag_count
        tag_index_count = None
        batched_datasets = RecommendDatasetBuilder.load_batched_datasets(dataset_name, config_name="plain_text")
        batched_dataset_features = RecommendDatasetBuilder.read_batched_datasets(batched_datasets)
        for features, labels in batched_dataset_features:
            tag_index_count = features['tag_index_count'][0]
            print(f"tag_index_count={features['tag_index_count']}")
            break
        return train_data, validation_data, evaluate_data, tag_index_count

    @print_exec_time
    def fit(self, *args, **kwargs):
        if not self.is_training_phase():
            return self
        loaded_dataset = kwargs.get("loaded_dataset")
        if loaded_dataset is not None:
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

    def serving(self, *args, **kwargs):
        return self

    @print_exec_time
    def predict_from_load_model(self, *args, **kwargs):
        """(线上已经使用改方法的子类实现)python版的预测接口，返回预测结果"""
        if not self.is_inference_phase():
            return None
        # restore weights from saved model file
        model = tf.keras.models.load_model(self.get_model_saved_dir() + "/saved_model.h5")
        self.log.info(f"already called load_model from: {self.get_model_saved_dir()}/saved_model.h5")
        member_id = kwargs.get("member_info")[0]
        user_content_list = kwargs.get("content_info_list")
        batch_size = 300
        inputs = {
            "member_id": np.array([1222] * batch_size),
            "content_id": np.array([33333] * 100 + [4444] * 100 + [5555] * 100),
            "gender": np.array([1.0] * batch_size),
            "age_group": np.array([2.0] * batch_size),
            "position": np.array([1.0] * batch_size),
            "annual_income": np.array([1.0] * batch_size),
            "address": np.array([0.0] * 300),
            "account_type": np.array([0.0] * batch_size),
            "asset_size": np.array([0.0] * batch_size),
            "Investment_risk_preference": np.array([1.0] * batch_size),
            "Market_preference": np.array([0.0] * batch_size),
            "content_type": np.array([2.0] * 100 + [1.0] * 100 + [0.0] * 100),
            "tag_indexs": np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                ] * 100 +
                [
                    [0.0, 128.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0]
                ] * 100 +
                [
                    [0.0, 334.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0]
                ] * 100
            )
        }
        predictions = model.predict(inputs)
        predictions = np.array([a[0] for a in predictions])
        recommended_content_scores = (-predictions).argsort()
        print(f"predictions={predictions}")
        print(f"用户Id：{member_id}")
        print(f"推荐的新闻Id的index列表,Top({len(user_content_list)})：{recommended_content_scores}")
        print(f"推荐得分倒序：{predictions[recommended_content_scores]}")
        return None

    @print_exec_time
    def predict_from_load_weights(self, *args, **kwargs):
        """python版的预测接口，返回预测结果"""
        if not self.is_inference_phase():
            return None
        # restore weights from latest checkpoint
        self.log.info(f"predict_from_load_weights#get_model_checkpoint_dir={self.get_model_checkpoint_dir()}")
        latest_checkpoint = tf.train.latest_checkpoint(self.get_model_checkpoint_dir())
        if latest_checkpoint:
            self.model.get_proxy().load_weights(latest_checkpoint)
            self.log.info(f"already called load_weights from: {latest_checkpoint}")
        # predict sample
        member_id = kwargs.get("member_info")[0]
        user_content_list = kwargs.get("content_info_list")
        inputs = {
            "member_id": np.array([1222]*300),
            "content_id": np.array([33333]*100 + [4444]*100 + [5555]*100),
            "gender": np.array([1.0]*300),
            "age_group": np.array([2.0]*300),
            "position": np.array([1.0]*300),
            "annual_income": np.array([1.0]*300),
            "address": np.array([0.0]*300),
            "account_type": np.array([0.0]*300),
            "asset_size": np.array([0.0]*300),
            "Investment_risk_preference": np.array([1.0]*300),
            "Market_preference": np.array([0.0]*300),
            "content_type": np.array([2.0]*100 + [1.0]*100 + [0.0]*100),
            "tag_indexs": np.array(
            [
            [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            ] * 100 +
            [
                [0.0, 128.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            ] * 100 +
            [
                [0.0, 334.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            ] * 100
            )
        }
        predictions = self.model.get_proxy().predict(inputs)
        predictions = np.array([a[0] for a in predictions])
        recommended_content_scores = (-predictions).argsort()
        print("predictions=", predictions)
        print("用户Id：", int(member_id))
        print("推荐的新闻Id的index列表,Top(" + str(len(user_content_list)) + ")：", recommended_content_scores)
        print("推荐得分倒序：", predictions[recommended_content_scores])
        return None

