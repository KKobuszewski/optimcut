#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division

import pytest
import numpy as np                                                        # Numpy
#import matplotlib.pyplot as plt                                           # Plottting

# import custom modules
import sys
sys.path.append('/home/konrad/Pulpit/Codes/optimcut')
import _optimcut

"""
usage: pytest -v test_optimcut.py
"""


def test_swap_order():
    x = np.array([1.0,2.0,3.0,4.0,5.0], dtype=np.float64, order='C')
    _optimcut.swap_order(x,testing=True) # NOTE: for testing this function always uses 
                                         #       the beginig of quasirandom sequence
    
    result = np.array([1.0, 5.0, 3.0, 4.0, 2.0]) # expected result
    
    assert np.allclose(x,result)

def test_double_swap():
    x = np.array([1.0,2.0,3.0,4.0,5.0], dtype=np.float64, order='C')
    y = x.copy()
    _optimcut.swap_order(x,testing=True) # NOTE: for testing this function always uses 
                                         #       the beginig of quasirandom sequence.
    _optimcut.swap_order(x,testing=True) # NOTE: double swap of same indices returns to
                                         #       the orginal variable
    assert np.allclose(x,y)
    


if __name__ == '__main__':
    
    x = np.array([1.0,2.0,3.0,4.0,5.0], dtype=np.float64, order='C')
    print(x)
    _optimcut.swap_order(x)
    print(x)
    _optimcut.swap_order(x)
    print(x)
