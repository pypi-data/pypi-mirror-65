#! /usr/bin/env python
__author__ = ["Raphael Leber"]
__copyright__ = "Copyright 2019, CPE Lyon"
__credits__ = ["Raphael Leber"]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "Template"

from .vehicule_parts.driving_system import DrivingSystem
from .vehicule_parts.lighting import Lighting
from .vehicule_parts.sensing import Sensing
from .vehicule_parts.canbus import CanBus

import pygame
from pygame.math import Vector2
from pygame.locals import *

import os


class Vehicule():

    SCALE = (240, 120)

    def __init__(self, x, y, angle, opt_no_CAN):
        self.driving_system = DrivingSystem(x, y, angle)
        self.lighting = Lighting(self.SCALE)
        self.sensing = Sensing()
        self.canbus = CanBus(None, opt_no_CAN)

        self.canbus.lighting = self.lighting
        self.canbus.sensing = self.sensing
        self.canbus.dbw_driving_system = self.driving_system
        
        # TODO ...

        #self.exit = False
        
        #dirpath = os.getcwd()


        current_dir = os.path.dirname(os.path.abspath(__file__))
        vehicle_path = os.path.join(current_dir, "Images/vehicules/car_blue.png")  

        self.car_image = pygame.image.load(vehicle_path)
        #self.rect = []
        #self.counter = 0
     


    def update(self, world, car_coords):
        self.canbus.update()
        
        self.lighting.update(world, self.driving_system.position, self.driving_system.angle, car_coords)
        self.driving_system.update()
         


        # The sensor is a rectangle of 60*60 px square around the car. Here we constantly update its position with the one of the car, update its sprite object and its group.
        self.sensing.image_segmentation.sensor_sprite.rect = pygame.Rect(self.driving_system.position.x, self.driving_system.position.y, 1, 1).inflate(60, 60)
        self.sensing.image_segmentation.sensor_sprite.rect.center = (self.driving_system.position.x , self.driving_system.position.y )
        self.sensing.image_segmentation.sensor_group.add(self.sensing.image_segmentation.sensor_sprite)

        self.sensing.update(world, world.obstacles, world.screen, self.driving_system.position, self.driving_system.angle, world.human.human_sprite)   


        # TODO ...   
        

  



if __name__ == "__main__":

    v = Vehicule()
    v.update()