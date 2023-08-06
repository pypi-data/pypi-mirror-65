 # -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages
from glob import glob
import syncnote

with open(glob('requirements.*')[0], encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if 'git+' not in x]

with open("README.md", "r", encoding='utf-8') as fr:
    long_description = fr.read()


setup(
       name = syncnote.version.name ,
       version=syncnote.__version__,
       description = " None" ,
       packages = find_packages(),
       include_package_data = True,

       long_description=long_description,
       long_description_content_type="text/markdown",
       author = "K.y" ,
       author_email="beidongjiedeguang@gmail.com",
       url = "https://github.com/beidongjiedeguang/SyncNote" ,
       license = "MIT" ,
       
       install_requires=install_requires,
       classifiers=[
                    'Operating System :: OS Independent',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Science/Research',
                    'Topic :: Scientific/Engineering :: Artificial Intelligence',
                    "Programming Language :: Python :: 3",
                    "Programming Language :: Python :: 3.5",
                    "Programming Language :: Python :: 3.6",
                    "Programming Language :: Python :: 3.7",
                    "Programming Language :: Python :: 3.8",
       ],
       keywords=[
          'Deep Learning',
          'Machine Learning',
          'Neural Networks',
          'Natural Language Processing',
          'Computer Vision'
      ]
)