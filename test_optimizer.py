#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division

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
    copt.make_iterations(_state=state,py_niter=10000,py_temp=10000) # make single iteration
    print(' next state:       ',copt.state)
    saves, costfs = copt.make_iterations(100,10000,save_states=True) # make single iteration
    print(' next state:       ',copt.state)
    
    material_id = _optimcut.material_ids_from_saves(saves, material_length)
    
    print()
    print()
    for it in range(saves.shape[0]):
        _str = ''
        for current_id in range( np.max(material_id[it,:])+1 ):
            _str += str( saves[it, np.where(material_id[it,:] == current_id)[0] ] ) + ' '
        print(saves[it,:], '\t', costfs[it], '\t', _str)
        #print(material_id[it,:])
    print()
    
    _optimcut.finalize_qrng()