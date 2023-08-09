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




if __name__ == '__main__':
    _optimcut.initialize_qrng()
    
    #
    state = np.array([1.0,2.0,3.0,4.0,5.0], dtype=np.float64, order='F')
    material_length = np.array([5.0,5.0,5.0,5.0,5.0], dtype=np.float64, order='C')
    
    
    print('# Test class CutOptimizer')
    copt = _optimcut.CutOptimizer(np.zeros(state.size),material_length)
    print(' material lengths: ',copt.material_length)
    print(' initial state:    ',copt.state)
    copt.make_iterations(_state=state,py_niter=1000,py_temp=10000) # make single iteration
    print(' next state:       ',copt.state)
    copt.make_iterations(100,10000) # make single iteration
    print(' next state:       ',copt.state)
    
    
    
    
    
    _optimcut.finalize_qrng()