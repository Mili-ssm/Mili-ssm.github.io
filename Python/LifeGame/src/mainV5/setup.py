from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("mainV5.pyx",
                            compiler_directives={'language_level' : "3"}
                        ),
    include_dirs=[numpy.get_include()]
)
