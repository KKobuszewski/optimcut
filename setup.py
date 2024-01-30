import os
import sys
import numpy

from setuptools import setup, find_packages
from setuptools.extension import Extension
#from distutils.core import setup
#from distutils.extension import Extension
from Cython.Distutils import build_ext

# get the annotated file as well
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
from Cython.Build import cythonize


"""
usage: python setup.py build_ext --inplace
       python setup.py install --user
"""



print('Compiling for')
print(sys.version)
print()


dpath = os.path.dirname( os.path.abspath(__file__) )
print(dpath)


# should be compiled with static libraries
# gcc -Wl,-Bstatic -llib1 -llib2 file.c

ext_modules = [
    Extension( '_optimcut',
               sources             = [dpath + '/src/optimcut/_optimcut.pyx'],
               language            = 'c++',
               include_dirs        = [numpy.get_include(),'.'],
               extra_compile_args  = ['-std=c++11','-fopenmp','-pthread','-fPIC','-mtune=native','-march=native','-O3'],
               extra_link_args     = ['-fopenmp','-pthread'],
               libraries           = ['gsl','gslcblas','gomp','m'],
               library_dirs        = ['/usr/local/lib'],
               define_macros       = [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")] ),
]

compiler_directives = 

setup(
    name = 'optimcut',
    #cmdclass = {'build_ext': build_ext},
    zip_safe=False,            # Without these two options
    include_package_data=True, # PyInstaller may not find your C-Extensions
    packages = find_packages()
    ext_modules = cythonize( ext_modules, 
                             compiler_directives = {'language_level' : str( sys.version_info.major )} ),
)







"""
https://stackoverflow.com/questions/22851552/can-i-create-a-static-cython-library-using-distutils

https://stackoverflow.com/questions/47042483/how-to-build-and-distribute-a-python-cython-package-that-depends-on-third-party
https://pypi.org/project/wheel/

"""


