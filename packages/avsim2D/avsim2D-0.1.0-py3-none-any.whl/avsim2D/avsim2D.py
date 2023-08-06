#! /usr/bin/env python
# coding=utf-8

__author__ = ["Raphaël Leber"]
__copyright__ = "Copyright 2020, CPE Lyon"
__credits__ = [" "]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "draft"


import pygame
import pytmx
from .world import World
from .vehicule import Vehicule

import argparse

import logging


class AvSim2D():
    """Autonomous Vehicule Simulator 2D

    """


    def __init__(self, opt_no_CAN):
        """Initialisation of attributs
        
        """
        #pygame.init()
        
        #self.screen = pygame.display.set_mode((1280,720))

        self.clock = pygame.time.Clock()
        self.world = World()
        self.vehicule = Vehicule(26, 71.5, -90, opt_no_CAN)

        #self.vehicule.lighting.low_beam( True )

        #self.world.init_map()

        self.ticks = 0

        self.exit = False
        self.flag_design = True
        self.flag_world = True
        self.dial_pos = [207, 550 + 179]        


    def update(self):
        """ Update game

        """

        #At the begining, one time, call the design.update function to open the start menu and allow the car selection.
        if self.flag_design == True:
            #car_image = self.vehicule.load_car_image()
            self.flag_design = False


        #Initialisation of the dashboard, needles, scope and steering wheel
        #needle = self.design.load("needle")
        #rpm_needle = pygame.transform.scale(self.design.load("needle"), (100, 6))
        #rect_rpm_needle = rpm_needle.get_rect(center=(self.dial_pos[0] + 98, self.dial_pos[1] - 72))
        #rect_speed_needle = needle.get_rect(center=(self.dial_pos[0] - 53, self.dial_pos[1] + 33))
        #self.police = pygame.font.Font(None, 90)
        #self.txt_gear = self.police.render("0", True, (255, 255, 255))
        #steering_wheel = self.vehicule.load("steering_wheel")
        #steering_wheel_rect = steering_wheel.get_rect(center=(self.dial_pos[0] + 150, self.dial_pos[1] + 100))


        #pixel per unit ratio
        ppu = 8

        #Start the car when the ping is put on map, then false at beginning
        start_flag = False        

        #Main loop
        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                if event.type == pygame.MOUSEBUTTONUP:
                    #First click for car selection
                    self.ping_x = pygame.mouse.get_pos()[0]
                    self.ping_y = pygame.mouse.get_pos()[1]
                    start_flag = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.vehicule.driving_system.reset()
                if event.type == pygame.KEYDOWN and event.key ==  pygame.K_s:
                    self.vehicule.sensing.image_segmentation.draw_camera_field = not self.vehicule.sensing.image_segmentation.draw_camera_field

       

            # Onces the car is selected, initialisation of the map
            if self.flag_world == True:
                self.world.init_map()
                logging.info('... Init Map !')
                self.flag_world = False

            #self.vehicule.driving_system.position.x += 0.1
            #self.vehicule.driving_system.angle += 1
            #self.vehicule.driving_system.throttle = 100
            #self.vehicule.driving_system.steering = 20

            # Display the background, the car and the foreground. The car is rotated by its calculated angle from driving system
            self.vehicule.car_image = pygame.transform.scale(self.vehicule.car_image, (240, 120) )
            rotated = pygame.transform.rotate(self.vehicule.car_image, self.vehicule.driving_system.angle)
            car_rect = rotated.get_rect()

            self.world.update_map_back()

            car_coords = self.vehicule.driving_system.position * ppu - (car_rect.width / 2, car_rect.height / 2)


            self.world.screen.blit(rotated, car_coords)
            self.world.update_map_front()

            self.world.update()

            self.vehicule.update(self.world, car_coords)


            #Display all the blits done before
            pygame.display.flip()

            self.clock.tick(self.ticks)

        pygame.quit()






#if __name__ == "__main__":


