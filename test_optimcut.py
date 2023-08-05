#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division

import numpy as np                                                        # Numpy
import matplotlib.pyplot as plt                                           # Plottting


import sys
sys.path.append('/home/konrad/Pulpit/KL Nord/optimcut')

import _optimcut


if __name__ == '__main__':
    
    x = np.array([1.0,2.0,3.0,4.0,5.0], dtype=np.float64, order='C')
    print(x)
    _optimcut.swap_order(x)
    print(x)
    _optimcut.swap_order(x)
    print(x)
