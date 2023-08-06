# -*- coding: iso-8859-1 -*-

import os
import glob
from setuptools import setup
from setuptools import Extension
import versioneer

cmdclass=versioneer.get_cmdclass()
#cmdclass['build_ext']=build_ext

setup(name='bengali_letters',
      version=versioneer.get_version(),
      cmdclass=cmdclass,
      author='Matt Hilton',
      author_email='matt.hilton@mykolab.com',
      url="https://github.com/mattyowl/bengali_letters",
      classifiers=[],
      description='Quiz app for learning Bengali letters.',
      long_description="""Multiple choice quiz app for learning Bengali letters.""",
      packages=['bengali_letters'],
      scripts=['bin/bengali_letters'],
      install_requires=["numpy"]
)
