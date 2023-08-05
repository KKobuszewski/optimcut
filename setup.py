from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

# get the annotated file as well
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True


"""
usage: python setup.py build_ext --inplace
       python setup.py install --user
"""

ext_modules = [
    Extension( '_optimcut',
               sources            = ['_optimcut.pyx'],
               language           = 'c++',
               include_dirs       = [numpy.get_include(),'.'],
               extra_compile_args = ['-std=c++11','-fopenmp','-pthread','-fPIC','-mtune=native','-march=native','-O3'],
               extra_link_args    = ['-fopenmp','-pthread'],
               libraries          = ['gsl','gslcblas','gomp','m'],
               library_dirs       = ['/usr/local/lib'],
               define_macros      = [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")] ),
]
setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)

import os
import shutil

"""
srcfile = 'build/lib.linux-x86_64-2.7/_optimcut.so'
dstfile = './_optimcut.so'


assert not os.path.isabs(srcfile)
shutil.copy(srcfile, dstfile)
shutil.rmtree('build')
"""
