#!/usr/bin/env python

from distutils.core import setup

setup(name='imgproc',
      version='1.0',
      description='Python Distribution Utilities',
      author='Scott Swindell',
      author_email='scottswindell@email.arizona.edu',
	  package_dir = {'':'src'},
      py_modules = ['m4kproc'],
      scripts = ['scripts/combine_amps_m4k.py'],
     )

