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

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation



# https://cvanelteren.github.io/post/cython_templates/

# ========================================================  FILE PROCESSING  ============================================================

cdef extern from "optimcut.h" namespace "optimcut" nogil:
    void initialize(int seed)
    void finalize()
    void _swap_order[T](T* old_state, T* new_state, int n)
    void _cuts_to_material[T](T* state, int* material_id, T* material_length, int n)
    void _material_leftovers[T](T* state, int* material_id, T* material_length, T* leftovers, int n)
    void make_iterations[T](T* state, int* material_id, T* material_length, T* leftovers, 
                            const int niter, const T temp, const int n)
    void make_iterations_with_save[T](T* states, int* material_id, T* material_length, T* leftovers, T* costfs,
                               const int niter, const T temp, const int n)
    #int ...


cpdef initialize_qrng(seed=-1):
    cdef int c_seed = <int> seed
    initialize(c_seed)

cpdef finalize_qrng(seed=-1):
    finalize()

cpdef void swap_order( np.ndarray[np.float64_t,ndim=1,negative_indices=False,mode='c'] state,
                       py_bool testing = False ):
    if (testing is True):
        initialize(0)
    
    cdef int n = <int> state.size
    _swap_order[double](&state[0],&state[0], n) # NOTE: doing swap inplace
    
    if (testing is True):
        finalize()


def cuts_to_material( np.ndarray[np.float64_t,ndim=1,negative_indices=False,mode='c'] state,
                      np.ndarray[np.int32_t,  ndim=1,negative_indices=False,mode='c'] material_id,
                      np.ndarray[np.float64_t,ndim=1,negative_indices=False,mode='c'] material_length,
                      py_bool testing = False ):
    if (testing is True):
        initialize(0)
    
    cdef int  n     = <int>  state.size
    cdef int* c_ptr = <int*> &material_id[0] # need to convert pointer from np.int32_t explicitly?
    _cuts_to_material[double](&state[0], c_ptr, &material_length[0], n)

    if (testing is True):
        finalize()


def material_leftovers( np.ndarray[np.float64_t,ndim=1,negative_indices=False,mode='c'] state,
                        np.ndarray[np.int32_t,  ndim=1,negative_indices=False,mode='c'] material_id,
                        np.ndarray[np.float64_t,ndim=1,negative_indices=False,mode='c'] material_length,
                        np.ndarray[np.float64_t,ndim=1,negative_indices=False,mode='c'] leftovers,
                        py_bool testing = False ):
    if (testing is True):
        initialize(0)
    
    cdef int  n     = <int>  state.size
    cdef int* c_ptr = <int*> &material_id[0]
    _material_leftovers[double](&state[0],c_ptr, &material_length[0], &leftovers[0], n)
    
    if (testing is True):
        finalize()


"""
class CutOptimizer(object):
    def __init__(self, name, operator):
        self.name = name
        self.operator = operator

    def __call__(self, *operands):
        return self.operator(*operands)
"""

cdef class CutOptimizer:

    # Not available in Python-space:
    cdef double[::1]   c_state
    cdef int[::1]      c_material_id
    cdef double[::1]   c_material_length
    cdef double[::1]   c_leftovers
    cdef double[:,::1] c_saves
    cdef double[::1]   c_costfs

    # Available in Python-space:
    cdef public int n

    cdef public np.ndarray state
    cdef public np.ndarray material_id
    cdef public np.ndarray material_length
    cdef public np.ndarray leftovers
    cdef public np.ndarray saves
    cdef public np.ndarray costfs

    def __cinit__(self, np.ndarray _state, np.ndarray _material_length): # cannot be overloaded
        """
        TODO: _material_length could be single float or array of floats
        """
        self.n = <int> _state.size

        # memory allocation
        self.state           = np.empty(self.n, dtype=np.float64, order='C')
        self.material_id     = np.empty(self.n, dtype=np.int32,   order='C')
        self.material_length = np.empty(self.n, dtype=np.float64, order='C')
        self.leftovers       = np.empty(self.n, dtype=np.float64, order='C')

        self.saves  = None
        self.costfs = None
        
        self.state[:]           = _state[:]
        self.material_length[:] = _material_length[:]

        # memoryviews of numpy arrays
        self.c_state           = self.state
        self.c_material_id     = self.material_id
        self.c_material_length = self.material_length
        self.c_leftovers       = self.leftovers

        initialize(0) #???

        #print(self.state)
    
    def __dealloc__(self):
        finalize()

    def make_iterations(self,py_niter=1,py_temp=1.0,_state=None,save_states=False):
        cdef int    niter = <int>    py_niter
        cdef double temp  = <double> py_temp

        if (_state is not None) and (_state.ndim == 1):
            self.state[:] = _state[:]

        if (save_states is False):
            make_iterations[double](&(self.c_state[0]), 
                                    &(self.c_material_id[0]), 
                                    &(self.c_material_length[0]), 
                                    &(self.c_leftovers[0]),
                                      niter, temp, self.n)
            return self.state
        else:
            # allocate memory to save consecutive states of algorithm & initialize the first state
            self.saves      = np.empty([niter+1,self.n],dtype=np.float64,order='C')
            self.saves[0,:] = self.state[:]
            self.costfs     = np.empty(niter+1,dtype=np.float64,order='C')
            
            # set memoryviews
            self.c_saves  = self.saves
            self.c_costfs = self.costfs
            
            # perform iterations
            make_iterations_with_save[double](&(self.c_saves[0,0]), 
                                              &(self.c_material_id[0]), 
                                              &(self.c_material_length[0]), 
                                              &(self.c_leftovers[0]), 
                                              &(self.c_costfs[0]),
                                                niter, temp, self.n)
            
            return self.saves, self.costfs
    
    def set_state(self,state):
        if (state is not None) and (state.ndim == 1):
            self.state[:] = state[:]

    # Available in Python-space:
    """
    @property
    def state(self):
        return self.state
    
    @property
    def period(self):
        return 1.0 / self.freq

    @period.setter
    def period(self, value):
        self.freq = 1.0 / value
    """
    #

def material_ids_from_saves(np.ndarray[np.float64_t,ndim=2,negative_indices=False,mode='c'] saves,
                            np.ndarray[np.float64_t,ndim=1,negative_indices=False,mode='c'] material_length):

    # NOTE: [np.ndarray] causes error (see: https://stackoverflow.com/questions/35414980/cython-dimensions-is-not-a-member-of-tagpyarrayobject)
    cdef int  n     = <int>  material_length.size
    cdef int  niter = <int> (saves.size // n)

    cdef np.ndarray[np.int32_t,ndim=2,negative_indices=False,mode='c'] material_ids = np.empty([niter,n], 
                                                                                               dtype=np.int32,
                                                                                               order='C')
    
    cdef int* c_material_ids
    cdef double* c_saves

    for it in range(niter):
        c_material_ids = <int*>    &material_ids[it,0]
        c_saves        = <double*> &saves[it,0]
        _cuts_to_material[double](c_saves, c_material_ids, &material_length[0], n)
    
    return material_ids





def visualize_algorithm(saves, material_ids, material_length,fps=30):
  # prepare figure
  fig, ax = plt.subplots()
  ax.set_xlim([0, max( [material_length.size+1,5] )])
  ax.set_xlabel("Material ID")
  ax.set_ylabel("Material length")
  cmap = mpl.colormaps['viridis']
  norm = mpl.colors.Normalize(vmin=0, vmax=int(material_length.max())+1)

  # draw material (setup background)
  for uid,ml in enumerate(material_length):
    p = ax.bar(uid+1, ml, fill=False, edgecolor='black')

  ims = []
  for it in range( saves.shape[0] ):

    order = saves[it,:]
    xs      = []
    heights = []
    bottoms = []
    for uid in np.unique(material_ids[it,:]):
      bottom=0
      order_id = order[material_ids[it,:]==uid]

      for (i,id_) in enumerate(order_id):
        xs.append(uid+1)
        heights.append(id_)
        bottoms.append(bottom)
        bottom += id_

    # draw slices
    barcollection = ax.bar(xs, heights, bottom=bottoms, color=cmap(norm(xs)), edgecolor='darkgrey')
    ims.append(barcollection)
  #
  ani = matplotlib.animation.ArtistAnimation(fig, ims, interval=1000/fps, blit=True,repeat_delay=1000)
  return ani.to_html5_video()
