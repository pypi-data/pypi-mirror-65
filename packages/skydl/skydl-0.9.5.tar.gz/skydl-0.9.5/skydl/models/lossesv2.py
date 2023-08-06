# coding=utf-8
from six import with_metaclass
from abc import ABCMeta, abstractmethod
from py_common_util.common.annotations import PublicAPI


@PublicAPI
class LossV2(with_metaclass(ABCMeta)):
    """
    自定义loss
    """
    def __init__(self, loss_func=None):
        # super().__init__(loss_func=loss_func)
        self.loss_func = loss_func

    def forward(self, y_true, y_pred, **kwargs):
        """
        :param y_true: 实际target的Tensor, 注意可能需要keras int32 -> tf float32
        :param y_pred: 预测target的Tensor, 注意可能需要keras int32 -> tf float32
        :param kwargs: other args
        :return:
        """
        return None

    def __call__(self, y_true, y_pred, **kwargs):
        """
        layer = XXLossV2()
        有了__call__方法就可以方便直接调用model(batch_x, parser_args=self.parser_args)方法
        来执行下面forward方法的内容
        :param y_true: 实际target的Tensor, 注意可能需要keras int32 -> tf float32
        :param y_pred: 预测target的Tensor, 注意可能需要keras int32 -> tf float32
        :param kwargs: other args
        :return:
        """
        if self.loss_func:
            return self.loss_func(y_true, y_pred)
        else:
            return self.forward(y_true, y_pred)

    def backward(self, grad):
        raise NotImplementedError

