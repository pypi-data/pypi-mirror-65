#!/usr/bin/env python

try:
    from setuptools import setup
    import setuptools
except ImportError:
    from distutils.core import setup

def readme():
  with open("README.md") as f:
    README = f.read()
  return README

setup(name='avsim2D',
  version='0.1.0',
  author='Raphael LEBER',
  description='A simple 2D autonomous vehicule simulator',
  long_description=readme(),
  long_description_content_type="text/markdown",
  url='https://gitlab.com/m0rph03nix/autonomous_vehicule_simulator',
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX :: Linux",
  ],
  python_requires='>=3.6',
  install_requires=[
    'pygame>=1.9.6',
    'pylint>=2.4.4',
    'python-can>=3.2.1a0',
    'PyTMX>=3.21.7',
    'PyYAML>=5.3'
  ],
  package_data= {'avsim2D':  ['*.png', 
                              '*.jpg', 
                              '*.yml',
                              'Images/*',
                              'Images/**/*',
                              'Images/vehicle_parts/*', 
                              'Images/vehicles/car_blue.png', 
                              'Images/vehicle_parts/*', 
                              'Images/human.png',
                              'Images/human_back.png',
                              'tiled/*'
                            ]
                }
)
