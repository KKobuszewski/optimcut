#distutils: language = c++
#cython: boundscheck=False, nonecheck=False, cdivision=True
from __future__ import print_function, division

cimport cython
cimport numpy as np
import numpy as np

from cpython cimport bool as py_bool
from libcpp cimport bool
from libc.stdio cimport printf

#from libcpp.algorithm cimport max_element
#cdef extern from "<algorithm>" namespace "std":




# ========================================================  FILE PROCESSING  ============================================================

cdef extern from "optimcut.h" namespace "optimcut" nogil:
    void initialize(int seed);
    void finalize();
    void _swap_order[T](T* state, int n);
    #int ...


cpdef void swap_order(np.ndarray[np.float64_t,ndim=1,negative_indices=False,mode='c'] state,
                      py_bool testing = True):
    if (testing is True):
        initialize(0)
    
    cdef int n = <int> state.size
    _swap_order[double](&state[0], n)
    
    if (testing is True):
        finalize()
