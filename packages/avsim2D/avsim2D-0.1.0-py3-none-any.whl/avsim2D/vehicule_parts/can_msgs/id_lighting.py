#! /usr/bin/env python
__author__ = ["Raphael Leber"]
__copyright__ = "Copyright 2020, CPE Lyon"
__credits__ = ["Raphael Leber"]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "Template"

import os
import logging
import can
from .id_can_abstract import id_CanAbstract

class id_Lighting(id_CanAbstract):
    """ Parse Lighting CAN frame """

    def __init__(self, lighting):
        self.lighting = lighting
        pass


    def parse(self, frame):

        if hasattr(frame, 'data') :
            data = frame.data

            if len(data) >=1 :
                if data[0] & 3 == 2:
                    logging.info("Switch On High Beam")
                    self.lighting.high_beam( True )
                    self.lighting.low_beam( False )
                elif data[0] & 3 == 1:
                    logging.info("Switch On Low Beam")
                    self.lighting.low_beam( True )
                    self.lighting.high_beam( False )
                else:
                    logging.info("Switch Off Beam")
                    self.lighting.low_beam( False )
                    self.lighting.high_beam( False )    

            if len(data) >=2 :
                if data[1] & 3 == 1:
                    logging.info("Blink Right")
                    self.lighting.blink_right( True )
                    self.lighting.blink_left( False )
                elif data[1] & 3 == 2:
                    logging.info("Blink Left")
                    self.lighting.blink_left( True )
                    self.lighting.blink_right( False )       
                elif data[1] & 3 == 3:
                    logging.info("Blink Right & Left")
                    self.lighting.blink_left( True )
                    self.lighting.blink_right( True )     
                else:
                    logging.info("Stop Blinking")
                    self.lighting.blink_left( False )
                    self.lighting.blink_right( False )                             



