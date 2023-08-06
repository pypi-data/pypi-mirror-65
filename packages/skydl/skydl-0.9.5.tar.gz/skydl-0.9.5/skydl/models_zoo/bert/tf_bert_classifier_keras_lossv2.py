# coding=utf-8
import tensorflow as tf
from skydl.models.lossesv2 import LossV2
from py_common_util.common.annotations import PublicAPI, Override


@PublicAPI
class TfBertClassifierKerasLossV2(LossV2):
    """Gets the Bert classification loss function."""
    def __init__(self, num_classes=2, loss_func=None):
        super().__init__(loss_func=loss_func)
        self.num_classes = num_classes

    @Override(LossV2)
    def forward(self, y_true, y_pred, **kwargs):
        """Classification loss."""
        loss_factor = 1.0
        labels = tf.squeeze(y_true)
        log_probs = tf.nn.log_softmax(y_pred, axis=-1)
        one_hot_labels = tf.one_hot(tf.cast(labels, dtype=tf.int32), depth=self.num_classes, dtype=tf.float32)
        per_example_loss = -tf.reduce_sum(tf.cast(one_hot_labels, dtype=tf.float32) * log_probs, axis=-1)
        loss = tf.reduce_mean(per_example_loss)
        loss *= loss_factor
        return loss
