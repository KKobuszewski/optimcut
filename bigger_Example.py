#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division

import numpy as np                                                        # Numpy
import scipy.integrate                                                    # 


import numpy as np                                                        # Numpy

#import matplotlib.pyplot as plt                                           # Plottting
#import matplotlib as mpl
#import matplotlib.animation


import sys
sys.path.append('/home/konrad/Pulpit/Codes/optimcut')
import _optimcut

state           = np.random.triangular(0, 250, 1000, 100)
material_ids    = np.zeros_like(state,dtype=np.int32)
material_length = np.zeros_like(state)+1000; material_length[0] = 1000;

#_optimcut.initialize_qrng()

copt = _optimcut.CutOptimizer(state,material_length)
print(' material lengths: ',copt.material_length)
print(' initial state:    ',copt.state)
saves, costfs = copt.make_iterations(_state=state,py_niter=10000,py_temp=100,save_states=True)

material_ids[:] = _optimcut.material_ids_from_saves(saves, material_length)

#_optimcut.finalize_qrng()
