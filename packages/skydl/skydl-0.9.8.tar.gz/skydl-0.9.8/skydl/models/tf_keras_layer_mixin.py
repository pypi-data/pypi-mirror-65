# -*- coding: utf-8 -*-
import tensorflow as tf
from tensorflow import keras


class TfKerasLayerMixin(keras.layers.Layer):

    def __init__(self, units=None, activation=None, **kwargs):
        """
        :param units: e.g. 10
        :param activation: e.g. python function or str: "softmax"|"relu" or wrapped by @tf.function
        :param kwargs: other args
        """
        super().__init__()
        self.activation = keras.layers.Activation(activation)
        self.units = units

    def build(self, input_shape):
        self.w = self.add_weight("W",
                                 shape=(input_shape[-1], self.units),
                                 # initializer='random_normal',
                                 trainable=True)
        self.b = self.add_weight("B",
                                 shape=(self.units,),
                                 # initializer='random_normal',
                                 trainable=True)

    def call(self, inputs):
        return self.activation(tf.matmul(inputs, self.w) + self.b)


