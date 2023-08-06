# -*- coding: utf-8 -*-
import sys
import os
from py_common_util.common.annotations import print_exec_time
from skydl.examples.modelsv2.playground_models.dummy_torch_modelv2 import DummyTorchModelV2
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))


@print_exec_time
def run_default_model():
    DummyTorchModelV2(
        "dummy_torch_modelv2"
    ).compile(
    ).fit()


if __name__ == '__main__':
    run_default_model()
