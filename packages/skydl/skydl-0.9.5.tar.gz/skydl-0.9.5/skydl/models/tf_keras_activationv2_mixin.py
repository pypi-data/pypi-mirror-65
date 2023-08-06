# -*- coding: utf-8 -*-
from tensorflow import keras


class TfKerasActivationV2Mixin(keras.layers.Activation):

    def __init__(self, activation, **kwargs):
        super().__init__(activation=activation, **kwargs)

    def call(self, inputs):
        return self.activation(inputs)
