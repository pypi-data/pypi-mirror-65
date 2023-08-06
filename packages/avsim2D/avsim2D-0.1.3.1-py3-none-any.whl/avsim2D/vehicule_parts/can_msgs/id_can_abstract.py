#! /usr/bin/env python
__author__ = ["Raphael Leber"]
__copyright__ = "Copyright 2020, CPE Lyon"
__credits__ = ["Raphael Leber"]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "Template"

from abc import ABCMeta, abstractmethod
import os
import can


class id_CanAbstract():
    """ Parse CAN frame Template"""

    def __init__(self, vehicule_part):
        pass

    @abstractmethod
    def parse(self, frame):
        pass




