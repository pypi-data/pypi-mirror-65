# -*- coding: utf-8 -*-
import tensorflow as tf
from py_common_util.common.annotations import PublicAPI, Override
from skydl.models.layersv2 import LayerV2
from skydl.models.tf_keras_activationv2_mixin import TfKerasActivationV2Mixin
from skydl.models.tf_keras_layer_mixin import TfKerasLayerMixin


def get_tf_gradient(x, activation_function):
    with tf.GradientTape() as gt:
        gt.watch(x)
        y = activation_function(x)
    gradient = gt.gradient(y, x).numpy()
    return gradient


@PublicAPI
class TfLayerV2(LayerV2):
    def backward(self, grad):
        print("TfLayerV2#backward(暂时没有用上自定义的backward)...")
        return get_tf_gradient(self.inputs, self.forward) * grad


@PublicAPI
class TfActivationLayerV2(TfLayerV2, TfKerasActivationV2Mixin):

    def __init__(self, activation=None, **kwargs):
        super().__init__()
        if activation is None:
            activation = self.forward
        TfKerasActivationV2Mixin.__init__(self, activation=activation, **kwargs)

    @Override(TfLayerV2)
    def call(self, *input, **kwargs):
        if self.activation:
            return TfKerasActivationV2Mixin.call(self, input[0])
        else:
            return self.forward(*input, **kwargs)


@PublicAPI
class TfReLU(TfActivationLayerV2):

    @Override(TfActivationLayerV2)
    def forward(self, *inputs, **kwargs):
        return tf.maximum(inputs[0], 0.0)


########################
@tf.function
def my_relu_def(x):
    return tf.maximum(x, 0.0)
print(f"@tf_function my_relu_def()生成的代码：{tf.autograph.to_code(my_relu_def.python_function, experimental_optional_features=None)}")
########################


class CustomDenseTfLayer(LayerV2, TfKerasLayerMixin):
    def __init__(self, units=None, activation=None, **kwargs):
        """
        :param units: e.g. 10
        :param activation: e.g. python function or keras built-in str: "softmax"|"relu"
        :param kwargs:
        """
        super().__init__()
        TfKerasLayerMixin.__init__(self, units=units, activation=activation, **kwargs)

    def forward(self, *inputs, **kwargs):
        return self.activation(tf.matmul(inputs[0], self.w) + self.b)



