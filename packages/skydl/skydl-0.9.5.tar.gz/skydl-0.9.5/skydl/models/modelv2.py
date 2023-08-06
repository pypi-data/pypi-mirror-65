# -*- coding: utf-8 -*-
import os
import sys
import argparse
import tensorflow as tf
from six import with_metaclass
from abc import ABCMeta, abstractmethod
from py_common_util.common.common_utils import CommonUtils
from py_common_util.common.annotations import PublicAPI, DeveloperAPI
from logbook import Logger, StreamHandler, FileHandler
from skydl.model.super_net import SuperNet
from skydl.models.train_phase_enum import TrainPhaseEnum
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))


@PublicAPI
class ModelV2(with_metaclass(ABCMeta)):
    """
    tf keras model
    注意：使用GPU需要显式设置pycharm IDE的环境变量(Environment Variables): PYTHONUNBUFFERED=1;PATH=/usr/local/cuda/bin:/home/user/anaconda3/bin:$PATH;LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/lib
    class WideDeepKerasMode(DefaultKerasModel):
    定义model class：
    class XxxKerasModel(DefaultKerasModel):
        def adjust_parse_args_value(self):
            super().adjust_parse_args_value()
        def load_data(self, *args, **kwargs):
            super().load_data(*args, **kwargs)
        def fit(self, *args, **kwargs):
            return self
        def evaluate(self, *args, **kwargs):
            return self
        def serving(self, *args, **kwargs):
            return self
        def predict(self, *args, **kwargs):
            if not self.is_inference_phase():
                return None
            return None

    调用例子如下：
    from tensorflow.python import keras
    MyKerasModel("my_keras_model", [
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax', name="prediction")
    ]).compile(
        keras.losses.sparse_categorical_crossentropy,
        keras.optimizers.Adam(),
        ['accuracy']
    ).fit().serving()
    ==========
    参考列表：
    https://www.tensorflow.org/alpha
    https://www.tensorflow.org/alpha/guide/saved_model#serving_the_model
    Training and Serving ML models with tf.keras  https://medium.com/tensorflow/training-and-serving-ml-models-with-tf-keras-fd975cc0fa27
    https://github.com/ray-project/ray/blob/master/python/ray/experimental/sgd/model.py
    https://colab.research.google.com
    将您的代码升级至 TensorFlow 2.0 https://mp.weixin.qq.com/s/BD-nJSZJLjBBq1n7HEHpKw
    tf2例子：https://github.com/tensorflow/docs/tree/master/site/en/r2/guide
    我的tf2训练场： https://colab.research.google.com/drive/1LtRP9lSivkdXJHX3S1_O8lFa9s21U6-V#scrollTo=ev01UBIHvaOj
    TensorFlow 2.0 Alpha 版发布啦！赶紧来尝鲜！https://mp.weixin.qq.com/s/gwcVOYhlEEBv28QoaFSnbw
    手工升级v1的代码到v2：$tf_upgrade_v2 --infile /Users/tony/myfiles/spark/share/python-projects/deep_trading/neural_networks/model/super_tf_model.py --outfile /Users/tony/myfiles/spark/share/python-projects/deep_trading/neural_networks/model/super_tf_model2.py
    """
    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, value):
        self._log = value

    @property
    def parser(self):
        return self._parser

    @property
    def parser_args(self):
        return self._parser_args

    @property
    def num_gpu(self):
        return self._num_gpu

    @property
    def device(self):
        """
        gpu设备数组，多个设备表示为[tf.device(),tf.device()]
        为充分利用gpu, batch_size必须设置尽量大
        :return:
        usage:
        .........
        with self.device:
            sum_operation = tf.reduce_sum(dot_operation)
            ......
        """
        return self._device

    @property
    def name(self):
        return self._name

    @property
    def model(self)->SuperNet:
        """
        定义SuperNet返回值类型便于IDE找到对应的静态类
        子类可以重写该方法的返回值类型便于IDE找到对应的静态类. e.g.
        @property
        def model(self)->estimator.Estimator:
            return self._model
        """
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def loss(self):
        """Return loss of the model
        Returns:
            loss
        """
        return self._loss

    @loss.setter
    def loss(self, value):
        self._loss = value

    @property
    def optimizer(self):
        """Return optimizer for the model
        Returns:
            optimizer
        """
        return self._optimizer

    @optimizer.setter
    def optimizer(self, value):
        self._optimizer = value

    @property
    def metrics(self):
        """Return metrics of the model
        Returns:
            metrics(dict): e.g. {"accuracy": accuracy(numpy data)}
        """
        return self._metrics

    @metrics.setter
    def metrics(self, value):
        self._metrics = value

    @property
    def weights(self):
        """Return weights from the model.
        Implementing `get_weights` is required for checkpointing and fault
        tolerance.
        Returns:
            Numpy array of weights from the model.
        """
        return self._weights

    @weights.setter
    def set_weights(self, value):
        self._weights = value

    @property
    def latest_model_filename(self):
        return "model.ckpt"

    @property
    def distribute_strategy(self):
        """
        多GPU分布式训练策略
        e.g. print('Number of devices: {}'.format(self.distribute_strategy.num_replicas_in_sync))
        """
        return self._distribute_strategy

    def __init__(self, name=None, loss=None, optimizer=None, metrics=None, weights=None):
        super().__init__()
        StreamHandler(sys.stdout).push_application()
        self._name = name
        self._log = Logger(self.name if self.name else self.__class__.__name__)
        self._parser = argparse.ArgumentParser()
        self._parser_args = None
        self._device = None
        self._num_gpu = 0
        self.do_parse_args()
        self._model = None if self.parser_args.lazy_load_model else self.build_network()
        # loss, optimizer, metrics, weights
        self._loss = loss
        self._optimizer = optimizer
        self._metrics = metrics
        self._weights = weights
        # distribute strategy, e.g. tf.distribute.MirroredStrategy(devices=self.device)
        self._distribute_strategy = tf.distribute.MirroredStrategy()
        self._load_data_fn = None

    def set_load_data_fn(self, load_data_fn):
        """
        允许设置外部加载数据的函数
        :param load_data_fn: e.g. def load_data_fn(parser_args)
        :return:
        """
        self._load_data_fn = load_data_fn
        return self

    @abstractmethod
    def build_network(self):
        """
        子类需要重写该方法
        :return: a net of SuperTfNets
        # super().build_network()
        """
        return SuperNet(self.name if self.name else 'super_net', self.parser_args)

    def _get_saved_model_with_version_dir(self):
        """
        获取带版本号的模型路径, e.g. "/home/user/ai_trained_models/recommend_ranking/20191106007/checkpoint/"
        :return:
        """
        saved_model_with_version_dir = self.parser_args.saved_model_path + "/" + self.model.name() + "/" + self.parser_args.model_version
        if not os.path.exists(saved_model_with_version_dir):
            os.makedirs(saved_model_with_version_dir)
        return saved_model_with_version_dir

    def get_model_checkpoint_dir(self):
        model_checkpoint_dir = self._get_saved_model_with_version_dir() + "/checkpoint"
        if not os.path.exists(model_checkpoint_dir):
            os.makedirs(model_checkpoint_dir)
        return model_checkpoint_dir

    def get_model_saved_dir(self):
        """
        整个model文件保存的目录：
        for tf.keras, 使用如：
        ```
        # save mode to h5
        model.save(self.get_trained_model_dir() + "/saved_model.h5")
        # restore model from h5
        model = tf.keras.models.load_model(self.get_trained_model_dir() + "/saved_model.h5")
        ```
        :return:
        """
        model_file_saved_dir = self._get_saved_model_with_version_dir() + "/saved_model"
        if not os.path.exists(model_file_saved_dir):
            os.makedirs(model_file_saved_dir)
        return model_file_saved_dir

    def get_model_logs_dir(self):
        """
        for tf.keras, 获取callback日志的路径
        :return:
        """
        model_logs_dir = self._get_saved_model_with_version_dir() + "/logs"
        if not os.path.exists(model_logs_dir):
            os.makedirs(model_logs_dir)
        return model_logs_dir

    def load_data(self):
        """
        load train|valid|test dataset
        子类需要重写该方法
        :return: batched_train_dataset, batched_validation_dataset, batched_evaluate_dataset
        """
        # super().load_data()
        if self._load_data_fn:
            return self._load_data_fn(self.parser_args)
        return None

    def add_parser_argument(self):
        """
        增加parser参数项
        子类需要重写该方法
        # super().add_parser_argument()
        """
        self.parser.add_argument('--init_from_saver', type=bool, default=True, metavar='N',
                            help='init from saved checkpoint')
        self.parser.add_argument('--fit_initial_epoch', type=int, default=0, metavar='0',
                            help='model will fit from [initial_epoch+1, epochs]，为了避免本次epoch中途报错退出时重启会从下一个epoch开始，也可以设置fit的initial_epoch参数为fit_initial_epoch-1')
        self.parser.add_argument('--saved_model_path', type=str, default=CommonUtils.get_user_home_path() + "/ai_trained_models",
                            help='save model data to path')
        self.parser.add_argument('--model_version', type=str, default='1',
                                 help='version number of the model, e.g. 20191106001')
        self.parser.add_argument('--train_phase', type=str, default=TrainPhaseEnum.Train.value,
                            help='train->train phase, test->test phase, inference->online inference phase, freeze->freeze model')
        self.parser.add_argument('--tf_summary_enabled', type=bool, default=False, metavar='N',
                            help='是否开启tensorflow的summary功能，注意在单机多GPU模式下开启该功能会让训练时间从24秒增加到107秒')
        self.parser.add_argument('--summary_path', type=str, default=sys.path[0] + '/summary',
                            help='dir where TensorBoard summary save to')
        self.parser.add_argument('--decay_rate', type=float, default=0.97, metavar='N',
                            help='decay rate for rmsprop, Decaying the learning rate)')
        self.parser.add_argument('--model', type=str, default='lstm',
                            help='（TODO 该参数将来可能被废弃）value of "cnn|lstm|bilstm", if bilstm then should set--num-hidden=2 else --num-hidden=1')
        self.parser.add_argument('--channels', type=int, default=1, metavar='N',
                            help='channels (i.e. depth, default: 1)')
        self.parser.add_argument('--height', type=int, default=28,
                            help='height')
        self.parser.add_argument('--width', type=int, default=28,
                            help='width')
        self.parser.add_argument('--num_classes', type=int, default=10,
                            help='num of classes')
        self.parser.add_argument('--time_steps', type=int, default=28,
                            help="time steps num of RNN, default equals to height's value, also equals to seq_length")
        self.parser.add_argument('--rnn_input', type=int, default=28,
                            help="RNN input(the value as same as width)")
        self.parser.add_argument('--rnn_hidden', type=int, default=256,
                            help="num of RNN hidden_layer or state size, default value is multiple of batch_size's value")
        self.parser.add_argument('--num_hidden', type=int, default=1,
                            help="num of n_hidden, for RNN, default value is 1: using rnn.static_bidirectional_rnn")
        self.parser.add_argument('--keep_prob', type=float, default=0.5,
                                 help="dropout: keep probability, default value is: 0.5")
        # 以下变量和pytorch共用
        self.parser.add_argument('--data_path', type=str, default=sys.path[0] + '/datasets',
                            help='location of the loading data corpus')
        self.parser.add_argument('--onnx_export_path', type=str, default=sys.path[0] + '/saved_model',
                                 help='path to export the final model in onnx format')
        self.parser.add_argument('--batch_size', type=int, default=64, metavar='N',
                            help='input batch size for training (default: 64)')
        self.parser.add_argument('--eval_batch_size', type=int, default=1000, metavar='N',
                            help='input batch size for testing (default: 1000)')
        self.parser.add_argument('--epochs', type=int, default=1, metavar='N',
                            help='number of epochs to train (default: 10)')
        self.parser.add_argument('--learning_rate', type=float, default=0.001, metavar='LR',
                            help='learning rate (default: 0.001)')
        self.parser.add_argument('--momentum', type=float, default=0.5, metavar='M',
                            help='SGD momentum (default: 0.5)')
        self.parser.add_argument('--use_cuda', action='store_true', default=True,
                            help='use CUDA')
        self.parser.add_argument('--seed', type=int, default=1, metavar='S',
                            help='random seed (default: 1)')
        self.parser.add_argument('--log_interval', type=int, default=1000, metavar='N',
                            help='how many batches to wait before logging training status')
        self.parser.add_argument('--lazy_load_model', type=bool, default=False, metavar='N',
                             help='lazy load model(build_network())')

    def adjust_parse_args_value(self):
        """
        调整pare_args参数的值
        子类需要重写该方法
        修改parser_args的值
        # super().adjust_parse_args_value()
        e.g. self.parser_args.seed = 1
        参考代码：
        def adjust_parse_args_value(self):
            super().adjust_parse_args_value()
            self.parser_args.data_path = sys.path[0] + '/../../datasets'
            self.parser_args.use_cuda = True
            self.parser_args.init_from_saver = True
            self.parser_args.fit_initial_epoch = 0
            self.parser_args.train_phase = TrainPhaseEnum.Train.value
            self.parser_args.model_version = '1'
            self.parser_args.epochs = 1
            self.parser_args.batch_size = 128
            self.parser_args.log_interval = 1000
        """
        pass

    def do_parse_args(self):
        self.add_parser_argument()
        self._parser_args = self.parser.parse_args()
        self.adjust_parse_args_value()
        # 子类将补充其它参数逻辑
        # subclass's do_parse_args func will call: super().do_parse_args()

    @DeveloperAPI
    def is_training_phase(self):
        return self.parser_args.train_phase == TrainPhaseEnum.Train.value

    @DeveloperAPI
    def is_evaluation_phase(self):
        return self.parser_args.train_phase == TrainPhaseEnum.Evaluate.value

    @DeveloperAPI
    def is_inference_phase(self):
        return self.parser_args.train_phase == TrainPhaseEnum.Inference.value

    @DeveloperAPI
    def can_compile(self):
        return self.is_training_phase() or self.is_evaluation_phase()

    @DeveloperAPI
    def compile(self, loss=None, optimizer=None, metrics=None):
        """
        Configures the model for training
        compile a model before training/testing
        inference阶段不需要调用模型的compile函数
        @see keras.models.Model.compile()
        :param loss:
        :param optimizer:
        :param metrics:
        :return: self
        """
        if self.parser_args.lazy_load_model:
            self.model = self.build_network()
        return self

    def fit(self, *args, **kwargs):
        """
        模型训练的启动入口
        子类需要重写该方法
        Training settings: 设置一些参数，每个都有默认值，输入 $python3 main.py -h 可以获得相关帮助
        $python3 main.py -batch_size=32 -log_interval=20
        :return: self
        """
        if not self.is_training_phase():
            return self
        return self

    def evaluate(self, *args, **kwargs):
        """
        在测试阶段测试训练好的模型效果
        @:param evaluate_dataset:测试数据集, shape: [num_batched, batch_size, feature_size,label_size]
        :return: self
        ```
        usage:
         evaluate(evaluate_dataset=[]) then: evaluate_dataset = kwargs.get("evaluate_dataset")
         evaluate([]) then: evaluate_dataset = args[0])
        ```
        """
        return self

    def serving(self):
        """
        build serving model
        用docker serving开启服务
        client可以使用java直接调用模型
        :return: self
        """
        return self

    def predict(self, *args, **kwargs):
        """python版的预测接口，返回预测结果"""
        return None
