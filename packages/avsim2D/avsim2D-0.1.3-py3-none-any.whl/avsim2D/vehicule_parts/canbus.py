#! /usr/bin/env python
__author__ = ["Raphael Leber"]
__copyright__ = "Copyright 2019, CPE Lyon"
__credits__ = ["Raphael Leber"]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "Template"

import os
import sys
import pygame

import yaml
import can

import asyncio

from .can_msgs.id_lighting import id_Lighting
from .can_msgs.id_dbw import id_DBW


class CanBus():
    """ Manage can bus """


    def __init__(self, can_handle, opt_no_CAN):
        
        self.dbw_driving_system = None
        self.lighting = None
        self.sensing = None

        self.canbus = {}


        if opt_no_CAN == "True":
            self.canbus["can_dbw"] = can.interface.Bus(bustype="virtual", channel="slcan0", bitrate=250000)

        else:

            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, "../config.yml")           

            try:
                print('TRY')
                with open("/tmp/avsim2D/config.yml", 'r') as ymlfile:
                    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader )    
            except:          
                print('EXCEPT')
                with open( config_path, 'r') as ymlfile:
                    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader )  

            for section in cfg:
                if "can_" in section:
                    self.canbus[section] = can.interface.Bus(bustype=cfg[section]["bustype"], channel=cfg[section]["channel"], bitrate=cfg[section]["bitrate"])
        

    def update(self):
        """ Update can frames """
        
        self.can_map =   {   
                        291 : id_Lighting(self.lighting), 
                        801 : id_DBW(self.dbw_driving_system)
                    }             
        
        for _,bus in self.canbus.items():
            if bus:

                
                msg = "something"
                while( msg != None):
                    msg = bus.recv(0.0001)

                    if hasattr(msg, 'arbitration_id') :

                        if msg.arbitration_id in self.can_map:
                            self.can_map[msg.arbitration_id].parse(msg)


        #send_driving_system_fb()
        #send_us_sensor()
        
        self.send_camera_segmentation_sensor( self.sensing, self.canbus['can_dbw'] )
        self.send_driving_fb(self.dbw_driving_system, self.canbus['can_dbw'])




    def send_camera_segmentation_sensor(self, sensing, canbus):

        can_data_fd = []
              

        for i, zone in enumerate(sensing.image_segmentation.zone):
            data = sensing.image_segmentation.semantic_sensor[zone]
            
            can_data = ( int(x) for x in data.__dict__.values() )

            msg = can.Message(arbitration_id=3072+i,
                            data=  can_data ,
                            is_extended_id=True)            
            canbus.send(msg)  

            can_data_fd.extend(can_data)

        """
        msg = can.Message(arbitration_id=0xd00,
                            data=  can_data_fd ,
                            is_extended_id=True)            
        canbus.send(msg)
        """

        pass


    def send_driving_fb(self, ds, canbus):

        motor_speed = int(ds.motor_speed)
        motor_speed_bytes = motor_speed.to_bytes(2, sys.byteorder)
        motor_speed_bytearray = bytearray(motor_speed_bytes)


        can_data = (int(ds.car_speed), int(ds.gear))

        msg = can.Message(  arbitration_id=3078,
                            data=  motor_speed_bytearray ,
                            is_extended_id=True)    

        canbus.send(msg)                  


        msg = can.Message(  arbitration_id=3079,
                            data=  can_data ,
                            is_extended_id=True)                                    

        canbus.send(msg)  






