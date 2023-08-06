# -*- coding: utf-8 -*-
# @Author  : DevinYang(pistonyang@gmail.com)
__all__ = ['Swish']

from .functional import swish
from torch import nn
from torch.nn import functional as F


class Swish(nn.Module):
    """Switch activation from 'SEARCHING FOR ACTIVATION FUNCTIONS'
        https://arxiv.org/pdf/1710.05941.pdf

        swish =  x / (1 + e^-beta*x)
        d_swish = (1 + (1+beta*x)) / ((1 + e^-beta*x)^2)

    """

    def __init__(self, beta=1.0):
        super(Swish, self).__init__()
        self.beta = beta

    def forward(self, x):
        return swish(x, self.beta)


class HardSwish(nn.Module):
    def __init__(self, inplace=False):
        super(HardSwish, self).__init__()
        self.inplace = inplace

    def forward(self, x):
        return x * F.relu6(x + 3., inplace=self.inplace) / 6.


class HardSigmoid(nn.Module):
    def __init__(self, inplace=False):
        super(HardSigmoid, self).__init__()
        self.inplace = inplace

    def forward(self, x):
        return F.relu6(x + 3., inplace=self.inplace) / 6.


class Activation(nn.Module):
    def __init__(self, act_type, **kwargs):
        super(Activation, self).__init__()
        if act_type == 'relu':
            self.act = nn.ReLU(**kwargs)
        elif act_type == 'relu6':
            self.act = nn.ReLU6(**kwargs)
        elif act_type == 'h_swish':
            self.act = HardSwish(**kwargs)
        elif act_type == 'h_sigmoid':
            self.act = HardSigmoid(**kwargs)
        elif act_type == 'swish':
            self.act = Swish(**kwargs)
        elif act_type == 'sigmoid':
            self.act = nn.Sigmoid()
        elif act_type == 'lrelu':
            self.act = nn.LeakyReLU(**kwargs)
        elif act_type == 'prelu':
            self.act = nn.PReLU(**kwargs)
        else:
            raise NotImplementedError('{} activation is not implemented.'.format(act_type))

    def forward(self, x):
        return self.act(x)
