# -*- coding: utf-8 -*-
import torch.nn as nn


class TorchModelV2Mixin(nn.Module):
    """
    default torch model wrapper
    """

    @property
    def logits(self):
        return self._logits

    def __init__(self):
        self._logits = None
        super().__init__()

    def forward(self, *input):
        self._logits = super().forward(input)
        return self._logits
