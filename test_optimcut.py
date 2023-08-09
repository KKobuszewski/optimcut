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


state           = np.array([1.0,2.0,3.0,4.0,5.0], dtype=np.float64, order='C')
material_id     = np.array([  0,  0,  0,  0,  0], dtype=np.int32,   order='C')
material_length = np.array([5.0,5.0,5.0,5.0,5.0], dtype=np.float64, order='C')
leftovers       = np.array([0.0,0.0,0.0,0.0,0.0], dtype=np.float64, order='C')



@pytest.mark.single_function
def test_swap_order():
    x = state.copy()
    _optimcut.swap_order(x,testing=True) # NOTE: for testing this function always uses 
                                         #       the beginig of quasirandom sequence

    result = np.array([1.0, 5.0, 3.0, 4.0, 2.0], dtype=np.float64, order='C') # expected result
    
    assert np.allclose(x,result)

@pytest.mark.single_function
def test_double_swap():
    x = state.copy()
    y = x.copy()
    _optimcut.swap_order(x,testing=True) # NOTE: for testing this function always uses 
                                         #       the beginig of quasirandom sequence.
    _optimcut.swap_order(x,testing=True) # NOTE: double swap of same indices returns to
                                         #       the orginal variable
    assert np.allclose(x,y)

@pytest.mark.single_function
def test_cuts_to_material():
    x = material_id.copy()
    
    _optimcut.cuts_to_material(state, x, material_length, testing=True)
    result = np.array([0,0,1,2,3], dtype=np.int32, order='C')
    
    assert np.all( x == result )

@pytest.mark.single_function
def test_leftovers():
    _optimcut.cuts_to_material(state, material_id, material_length, testing=True)
    _optimcut.material_leftovers(state, material_id, material_length, leftovers, testing=True)
    
    result = np.array([2.0, 2.0, 1.0, 0.0, 0.0,], dtype=np.float64, order='C') # expected result
    
    assert np.allclose(leftovers,result)



if __name__ == '__main__':
    
    x = np.array([1.0,2.0,3.0,4.0,5.0], dtype=np.float64, order='C')
    print('# Double swap order test')
    print(x)
    _optimcut.swap_order(x,testing=True)
    print(x)
    _optimcut.swap_order(x,testing=True)
    print(x)
    print()
    
    
    print('# Cuts to material id test')
    material_id     = np.array([0,0,0,0,0], dtype=np.int32, order='C')
    material_length = np.array([5.0,5.0,5.0,5.0,5.0], dtype=np.float64, order='C')
    _optimcut.cuts_to_material(x, material_id, material_length, testing=True )
    print(material_id)
    print()
    
    print('# Test leftovers')
    leftovers      = np.array([0.0,0.0,0.0,0.0,0.0], dtype=np.float64, order='C')
    _optimcut.material_leftovers(x, material_id, material_length, leftovers, testing=True )
    print(leftovers)
    print()
    
    print('# Test class CutOptimizer')
    state = np.array([1.0,2.0,3.0,4.0,5.0], dtype=np.float64, order='F')
    _optimcut.initialize_qrng()
    copt = _optimcut.CutOptimizer(state,material_length)
    print(' material lengths: ',copt.material_length)
    print(' initial state:    ',copt.state)
    copt.make_iterations(100,10000) # make single iteration
    print(' next state:       ',copt.state)
    copt.make_iterations(100,10000) # make single iteration
    print(' next state:       ',copt.state)
    _optimcut.finalize_qrng()
    
    """
    x = np.array([1.0,2.0,3.0,4.0,5.0], dtype=np.float64, order='C')
    print('# Multiple swap order test')
    print(x)
    _optimcut.initialize_qrng()
    for i in range(100):
        _optimcut.swap_order(x,testing=False)
        print(x)
    _optimcut.finalize_qrng()
    """
    
    
