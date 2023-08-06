# -*- coding: utf-8 -*-
import numpy as np
from six import with_metaclass
from abc import ABCMeta, abstractmethod
from py_common_util.common.annotations import PublicAPI


@PublicAPI
class LayerV2(with_metaclass(ABCMeta)):
    """
    自定义layer
    """
    def __init__(self):
        # self.inputs = None
        pass

    def forward(self, *inputs, **kwargs):
        # self.inputs = inputs[0]
        return None

    def call(self, *input, **kwargs):
        """
        layer = XXLayerV2()
        有了__call__方法就可以方便直接调用model(batch_x, parser_args=self.parser_args)方法
        来执行下面forward方法的内容
        :param input:
        :param kwargs:
        :return:
        """
        # print("TfLayerV2#__call__...")
        result = self.forward(*input, **kwargs)
        return result

    def backward(self, grad):
        # 暂时使用后端框架(如tensorflow,keras,pytorch)的自动微分机制
        raise NotImplementedError


@PublicAPI
class NumpyReLU(LayerV2):

    def __init__(self):
        super().__init__()
        self.inputs = None

    def forward(self, *inputs, **kwargs):
        self.inputs = None
        super().forward(*inputs, **kwargs)
        return np.maximum(self.inputs, 0.0)

    def backward(self, grad):
        return self._derivative(self.inputs) * grad

    def _derivative(self, x):
        return x > 0.0

