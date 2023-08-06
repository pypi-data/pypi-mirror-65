# -*- coding: utf-8 -*-
from skydl.models.netv2 import NetV2
from skydl.models.torch_modelv2_mixin import TorchModelV2Mixin


class TorchNetV2(NetV2, TorchModelV2Mixin):
    """pytorch net"""
    def __init__(self, name=None, parser_args=None):
        super().__init__(name=name, parser_args=parser_args)
        # 再显式调用其它的__init__(self)
        TorchModelV2Mixin.__init__(self)

    def forward(self, *input, **kwargs):
        return super().forward(*input, **kwargs)

    def call_hidden_layers(self, _x, name="predict"):
        name = 'predict' if name is None else name
        predict = None
        return predict

    def compile_loss_metrics_optimizer_predict(self, _x, _y, _learning_rate=0.001, devices=[]):
        pass
