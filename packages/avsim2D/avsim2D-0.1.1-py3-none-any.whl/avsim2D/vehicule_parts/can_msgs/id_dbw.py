#! /usr/bin/env python
__author__ = ["Raphael Leber"]
__copyright__ = "Copyright 2020, CPE Lyon"
__credits__ = ["Raphael Leber"]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "Template"

import os
import ctypes
import can
from .id_can_abstract import id_CanAbstract

class id_DBW(id_CanAbstract):
    """ Parse Drive By Wire CAN frame """

    def __init__(self, dbw):
        self.dbw = dbw
        pass


    def parse(self, frame):
        if hasattr(frame, 'data') :
            data = frame.data
                        #self.vehicule.driving_system.throttle = 100
            #self.vehicule.driving_system.steering = 20

            if len(data) >=1 :
                self.dbw.throttle = data[0]

            if len(data) >=2 :
                self.dbw.brake = data[1]

            if len(data) >=3 :
                self.dbw.steering =  ctypes.c_int8(data[2]).value 
                
    
        pass




