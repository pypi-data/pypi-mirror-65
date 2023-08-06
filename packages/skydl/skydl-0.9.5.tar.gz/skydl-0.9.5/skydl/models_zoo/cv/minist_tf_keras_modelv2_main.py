# -*- coding: utf-8 -*-
import sys
import os
from tensorflow import keras
from skydl.models.tf_keras_layersv2 import TfReLU, CustomDenseTfLayer, my_relu_def
from skydl.models.tf_keras_lossesv2 import CustomTfKerasLossV2
from skydl.models_zoo.cv.minist_tf_keras_modelv2 import MnistTfKerasModelV2
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))


def training_mnist_tf_keras_model():
    MnistTfKerasModelV2("mnist_tf_keras_modelv2", [
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dropout(0.1),
        CustomDenseTfLayer(units=128, activation=TfReLU(my_relu_def)),
        CustomDenseTfLayer(units=10, activation="softmax")
    ]).compile(
        loss=keras.losses.sparse_categorical_crossentropy,
        # loss=CustomTfKerasLossV2(),
        optimizer=keras.optimizers.Adam(),
        metrics=['accuracy']
        # ['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    ).fit()
