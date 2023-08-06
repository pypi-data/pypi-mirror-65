# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class TrainPhaseEnum(Enum):
    """
    train->test->->inference
    """
    Train = 'train'  # train phase
    Evaluate = 'evaluate'  # evaluate phase, i.e. test phase
    Inference = 'inference'  # online inference phase


if __name__ == '__main__':
    for name, phase in TrainPhaseEnum.__members__.items():
        print(name, '=>', phase, ',', phase.value)
