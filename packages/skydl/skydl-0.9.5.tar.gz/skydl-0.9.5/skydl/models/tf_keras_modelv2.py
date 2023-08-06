# -*- coding: utf-8 -*-
import os,sys
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from py_common_util.common.annotations import PublicAPI, Override
from py_common_util.tensorflow.tf_utils import TFUtils
from skydl.models.modelv2 import ModelV2
from tensorflow.python import keras  # 或from tensorflow import keras
from tensorflow_estimator import estimator  # estimator import方便查看源代码
from skydl.models.tf_keras_netv2 import TfKerasNetV2
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))


@PublicAPI
class TfKerasModelV2(ModelV2):
    """
    default tensorflow2 keras model implements
    see document(english): https://www.tensorflow.org/api_docs/python/tf
    see document(chinese): https://www.tensorflow.org/api_docs/python/tf?hl=zh-CN
    find a issue: Unable to use FeatureColumn with Keras Functional API #27416  https://github.com/tensorflow/tensorflow/issues/27416
    """
    @property
    @Override(ModelV2)
    def model(self)->keras.Sequential:
        """定义keras.Model返回值类型便于IDE找到对应的静态类"""
        return self._model

    def __init__(self, name=None, keras_layers=[], keras_inputs=None, keras_outputs=None, loss=None, optimizer=None, metrics=None, weights=None):
        self._keras_layers = keras_layers
        self._keras_inputs = keras_inputs
        self._keras_outputs = keras_outputs
        super().__init__(name=name, loss=loss, optimizer=optimizer, metrics=metrics, weights=weights)

    @Override(ModelV2)
    def build_network(self):
        return TfKerasNetV2(self.name if self.name else self.__class__.__name__, self.parser_args,
                               self._keras_layers, keras_inputs=self._keras_inputs, keras_outputs=self._keras_outputs)

    @Override(ModelV2)
    def compile(self, loss=keras.losses.sparse_categorical_crossentropy, optimizer=keras.optimizers.Adam(), metrics=["accuracy"]):
        if not self.can_compile():
            return self
        # with self.distribute_strategy.scope():  报错 ValueError: We currently do not support distribution strategy with a `Sequential` model that is created without `input_shape`/`input_dim` set in its first layer or a subclassed model.
        # with self.distribute_strategy.scope():
        self.loss = loss
        self.optimizer = optimizer
        self.metrics = metrics
        super().compile(loss=self.loss, optimizer=self.optimizer, metrics=self.metrics)
        self.model.get_proxy().compile(optimizer=self.optimizer,
                                       loss=self.loss,
                                       metrics=self.metrics)
        # self.log.info(self.model.get_proxy().summary())  # 训练mnist会碰到个issue: This model has not yet been built.
        # restore weights from latest checkpoint
        latest_checkpoint = tf.train.latest_checkpoint(self.get_model_checkpoint_dir())
        if self.parser_args.init_from_saver and latest_checkpoint:
            # parse saved last epoch number from checkpoint file
            # e.g. "/home/user/ai_trained_models/recommend_ranking/20191106024/checkpoint/0024-0.0518-model.ckpt"
            self.parser_args.fit_initial_epoch = int(os.path.split(latest_checkpoint)[1].split("-")[0])
            self.model.get_proxy().load_weights(latest_checkpoint)
            self.log.info(f"tf.keras already called load_weights from: {latest_checkpoint}, self.parser_args.fit_initial_epoch={self.parser_args.fit_initial_epoch}")
        return self

    @Override(ModelV2)
    def load_data(self):
        data = super().load_data()
        return data

    @Override(ModelV2)
    def fit(self, *args, **kwargs):
        if not self.is_training_phase():
            return self
        return self

    @Override(ModelV2)
    def evaluate(self, *args, **kwargs):
        if not self.is_training_phase() and not self.is_evaluation_phase():
            return self
        # 最后切换到TrainPhaseEnum.Evaluate阶段
        return self

    @Override(ModelV2)
    def serving(self, *args, **kwargs):
        # restore weights from latest checkpoint
        latest_checkpoint = tf.train.latest_checkpoint(self.get_model_checkpoint_dir())
        if latest_checkpoint:
            self.model.get_proxy().load_weights(latest_checkpoint)
            self.log.info("already called load_weights from: " + latest_checkpoint)
        saved_serving_path = self.parser_args.saved_model_path + "/serving/models/" + self.model.name() + "/" + self.parser_args.model_version

        _, evaluate_dataset, _ = self.load_data()
        # prediction mode
        for batched_examples in tfds.as_numpy(evaluate_dataset.take(1)):
            test_batched_features, test_batched_labels = batched_examples
        predictions = self.model.get_proxy().predict(test_batched_features)
        print("serving predict, real:", np.argmax(predictions[0]), test_batched_labels[0])

        # save model for tf serving
        if not self.model.get_proxy().inputs:
            for batched_examples in tfds.as_numpy(evaluate_dataset.take(1)):
                test_batched_features, test_batched_labels = batched_examples
                self.model.get_proxy()._set_inputs(test_batched_features)
        tf.saved_model.save(self.model.get_proxy(), saved_serving_path)
        return self

    @Override(ModelV2)
    def predict(self, *args, **kwargs):
        if not self.is_inference_phase():
            return None
        return None

    @Override(ModelV2)
    def do_parse_args(self):
        super().do_parse_args()
        # 设置random seed确保每次训练都可以获得相同唯一的的随机序列
        np.random.seed(self.parser_args.seed)
        tf.random.set_seed(self.parser_args.seed)
        self._num_gpu = TFUtils.check_available_gpus(show_info=True)
        if self.num_gpu > 0:
            if not self.parser_args.use_cuda:
                self.log.info(f"WARNING: You have {self.num_gpu} CUDA device, so you should probably run with --cuda")
                # 不使用GPU加速
                self._num_gpu = 0
        else:
            self.parser_args.use_cuda = False
        if self.parser_args.use_cuda:
            self._device = [TFUtils.device("gpu" if self.parser_args.use_cuda else "cpu", gpu_id) for gpu_id in range(self._num_gpu)]
        else:
            self._device = []
        self.log.info(f"Tensorflow Version: {tf.__version__ }\nMain function argparse: {self.parser_args}")

    def _fit_callbacks(self):
        """
        private method: keras fit callbacks
        see: https://www.tensorflow.org/tutorials/keras/save_and_load?hl=zh-CN
        :return:
        """
        # Function for decaying the learning rate.
        # You can define any decay function you need.
        def decay(epoch):
            if epoch < 3:
                return 1e-3
            elif 3 <= epoch < 7:
                return 1e-4
            else:
                return 1e-5

        class PrintLR(tf.keras.callbacks.Callback):
            def __init__(self, model_checkpoint_filename):
                self.model_checkpoint_filename = model_checkpoint_filename

            def on_epoch_end(self, epoch, logs=None):
                # TODO 保存模型的权重和偏置
                # #self.model.save_weights(self.model_checkpoint_filename)
                # this self is inner class self, so no need set self.model.get_proxy()
                print(f'\ntf.keras callbacks-PrintLR.on_epoch_end(): Learning rate for epoch {epoch+1} is {self.model.optimizer.lr.numpy()}')

        class EvaluateCallback(tf.keras.callbacks.Callback):
            """usage: callbacks=[TestCallback((X_test, Y_test), 512)]"""
            def __init__(self, evaluate_data, batch_size):
                self.evaluate_data = evaluate_data
                self.batch_size = batch_size
            def on_epoch_end(self, epoch, logs={}):
                x, y = self.evaluate_data
                loss, acc = self.model.evaluate(x, y, verbose=1, batch_size=self.batch_size)
                print('\nEvaluating loss: {}, acc: {}'.format(loss, acc))

        callbacks = [
            tf.keras.callbacks.TensorBoard(log_dir=self.get_model_logs_dir(), histogram_freq=0, write_graph=True, write_images=True),
            tf.keras.callbacks.LearningRateScheduler(decay),
            PrintLR(self.get_model_checkpoint_dir() + "/" + self.latest_model_filename),
            tf.keras.callbacks.ModelCheckpoint(filepath=self.get_model_checkpoint_dir() + "/{epoch:04d}-{loss:0.4f}-" + self.latest_model_filename, save_weights_only=True, verbose=1)
        ]
        return callbacks

    def _model_to_estimator(self, keras_model_path=None,
                           custom_objects=None,
                           model_dir=None,
                           config=None) -> estimator.Estimator:
        """
        private method，从编译的Keras模型创建Estimator，需要调用model_to_estimator方法
        注意：
        需要先执行compile()
        keras model subclass必须继承于超类keras.Sequential才能成功执行model_to_estimator()
        :return: estimator
        """
        # config = tf.estimator.RunConfig(train_distribute=self.distribute_strategy) # 报错：ValueError: Only TensorFlow native optimizers are supported with DistributionStrategy.
        # estimator = tf.keras.estimator.model_to_estimator(self.model, config=config)
        return keras.estimator.model_to_estimator(keras_model=self.model,
                                                   keras_model_path=keras_model_path,
                                                   custom_objects=custom_objects,
                                                   model_dir=model_dir,
                                                   config=config)
