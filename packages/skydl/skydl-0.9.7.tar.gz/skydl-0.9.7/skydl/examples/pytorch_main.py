# -*- coding: utf-8 -*-
import sys
import os
from py_common_util.common.annotations import print_exec_time
from skydl.model.impl.my_pytorch.my_pytorch_model import MyPyTorchModel
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))


@print_exec_time
def run_default_model():
    MyPyTorchModel(
        "my_torch_model"
    ).compile(
    ).fit()


if __name__ == '__main__':
    run_default_model()














