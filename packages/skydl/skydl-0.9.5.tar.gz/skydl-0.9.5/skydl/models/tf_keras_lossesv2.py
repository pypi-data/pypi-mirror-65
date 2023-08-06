# coding=utf-8
import tensorflow as tf
from skydl.models.lossesv2 import LossV2
from py_common_util.common.annotations import PublicAPI, Override


@PublicAPI
class CustomTfKerasLossV2(LossV2):

    @Override(LossV2)
    def forward(self, y_true, y_pred, **kwargs):
        y_true = tf.cast(y_true, tf.float32)
        y_pred = tf.cast(y_pred, tf.float32)
        return tf.reduce_mean(tf.square(tf.subtract(y_true, y_pred)))

