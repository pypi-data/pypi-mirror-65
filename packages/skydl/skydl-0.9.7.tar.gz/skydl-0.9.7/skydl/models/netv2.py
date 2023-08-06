# -*- coding: utf-8 -*-
from six import with_metaclass
from abc import ABCMeta, abstractmethod


class NetV2(with_metaclass(ABCMeta)):
    """
    由多个layer组成的网络
    usage:
    class MNISTTFNet(SuperTFNet):
        def __init__(self, name=None, parser_args=None):
            super().__init__(name, parser_args)
            self.conv1 = nn.Conv2d(1, 20, 5)
            self.conv2 = nn.Conv2d(20, 20, 5)

        def forward(self, x):
            super().forward(x)
            x = F.relu(self.conv1(x))
            return F.relu(self.conv2(x))
    """
    @property
    def parser_args(self):
        return self._parser_args

    def name(self):
        """
        子类可以重写该方法
        :return:
        # super().name()
        """
        return self._net_name if self._net_name else 'super_net'

    @property
    def model_proxy(self)->object:
        """
        model_proxy maybe None or keras.Model or torch.nn.Module
        子类可以重写该方法的返回值类型便于IDE找到对应的静态类. e.g.
        @property
        def model_proxy(self)->keras.Model:
            return self._model_proxy
        """
        return self._model_proxy

    def get_proxy(self):
        if self._model_proxy is None:
            return self
        return self._model_proxy

    def __init__(self, name=None, parser_args=None):
        """
        子类需要重写该方法
        :param name e.g. "mnist" 或 "gym_trading"
        # super().__init__(name, parser_args)
        """
        self._model_proxy = None
        self._net_name = name
        self._parser_args = parser_args

    @abstractmethod
    def forward(self, *input, **kwargs):
        """
        子类需要重写该方法
        目标函数，返回可以和target(label)对比的predict(logits)
        :param *input: tuple类型 input[0]->batch_x
        :param **kwargs: dict类型 kwargs.get("parser_args")->parser_args
        :return: result
        # super().forward(x)
        ......
        model = MNISTTFModel().build_network()
        result = model(batch_x)
        ......
        """
        # return self.call_hidden_layers(input[0], name=kwargs.get("name"))
        if len(input) < 1:  # for keras serving
            return self.call_hidden_layers(kwargs.get("inputs"))
        return self.call_hidden_layers(input[0])

    def __call__(self, *input, **kwargs):
        """
        model = MNISTTFModel().build_network()
        有了__call__方法就可以方便直接调用model(batch_x, parser_args=self.parser_args)方法
        来执行下面forward方法的内容
        :param input:
        :param kwargs:
        :return:
        """
        result = self.forward(*input, **kwargs)
        return result

    @abstractmethod
    def call_hidden_layers(self, _x):
        """
        子类可以重写该方法
        you can see: forward(input)
        :param _x: input
        :return predict
        """
        return None

    @abstractmethod
    def compile_loss_metrics_optimizer_predict(self, _x, _y, _learning_rate=0.001, devices=[]):
        """
        子类可以重写该方法
        Define loss(cost) and optimizer
        ref: The art of regularization  https://greydanus.github.io/2016/09/05/regularization/
        https://github.com/greydanus/regularization
        TensorFlow with multiple GPUs https://jhui.github.io/2017/03/07/TensorFlow-GPU/
        [TensorFlow笔记] TensorArray解析 https://blog.csdn.net/guolindonggld/article/details/79256018
        AutoGraph converts Python into TensorFlow graphs  https://medium.com/tensorflow/autograph-converts-python-into-tensorflow-graphs-b2a871f87ec7
        @FIXME 后续将该函数纳入@autograph.convert()，以使多GPU的train的模型在serving后的Inference阶段即使没有GPU的机器上也能正确执行模型graph
        如果accuracy为None, 则可以返回default_accuracy = tf.constant(0)
        :param _x:
        :param _y:
        :param _learning_rate: TODO 该参数将来可能被废弃
        :param devices: e.g. [] TODO 该参数将来可能被废弃
        :return: loss, accuracy, optimizer, _predict
        """
        return None, None, None, None

