#! /usr/bin/env python
__author__ = ["", ""]
__copyright__ = "Copyright 2019, CPE Lyon"
__credits__ = ["Raphael Leber"]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "Template"

import os
import pygame


class Lighting():
    """ Manage low beam, high beam, blink right, blink left """

    def __init__(self, scale):
        self._low_beam = False
        self._high_beam = False
        self._blink_left = False
        self._blink_right = False

        self.scale = scale

        self.blink_rate = 3
        self.blink_counter = self.blink_rate

        self.blink_left_cur_state = False # True to light ON, False to light OFF
        self.blink_right_cur_state = False # True to light ON, False to light OFF

        current_dir = os.path.dirname(os.path.abspath(__file__))

        low_beam_path = os.path.join( current_dir, "../Images/vehicule_parts/lowbeam.png")
        high_beam_path = os.path.join( current_dir, "../Images/vehicule_parts/highbeam.png")
        blink_left_path = os.path.join( current_dir, "../Images/vehicule_parts/blinkleft.png")
        blink_right_path = os.path.join( current_dir, "../Images/vehicule_parts/blinkright.png")
        car_path = os.path.join( current_dir, "../Images/vehicules/car.png")
        nolights_path = os.path.join( current_dir, "../Images/vehicule_parts/nolights.png")        


        self.low_beam_image = pygame.image.load( low_beam_path)
        self.high_beam_image = pygame.image.load( high_beam_path)
        self.blink_left_image = pygame.image.load( blink_left_path)
        self.blink_right_image = pygame.image.load( blink_right_path)
        self.car_image = pygame.image.load( car_path)
        self.nolights_image = pygame.image.load( nolights_path)        


    def low_beam(self, on_off):
        """ Swith low beam ON/OFF (Boolean) """
        self._low_beam = on_off
        if self._low_beam == True :
            self._high_beam = False

    def high_beam(self, on_off):
        """ Swith low beam ON/OFF (Boolean) """
        self._high_beam = on_off
        if self._high_beam == True :
            self._low_beam = False        

    def blink_left(self, on_off):
        """ Swith left blinker ON/OFF (Boolean) """
        self._blink_left = on_off
        #if self._blink_left == True :
        #    self._blink_right = False         

    def blink_right(self, on_off):
        """ Swith left blinker ON/OFF (Boolean) """
        self._blink_right = on_off
        #if self._blink_right == True :
        #    self._blink_left = False             

    def fit_light(self, world, position, angle, car_coords, image):
        """ Fit light on the car into the world """
        lights = pygame.transform.scale(image, self.scale )
        rotated_lights = pygame.transform.rotate(lights, angle)        
        world.screen.blit(rotated_lights, car_coords )        



    def update(self, world, position, angle, car_coords):
        """ Manage switch on/off """


        # Manage blinking
        if self.blink_counter > 0 :
            self.blink_counter -= 1
        else:
            self.blink_counter = self.blink_rate
            
            if  self._blink_left == True :
                self.blink_left_cur_state = not self.blink_left_cur_state
            else:
                self.blink_left_cur_state = False

            
            if self._blink_right == True :
                self.blink_right_cur_state = not self.blink_right_cur_state      
            else:
                self.blink_right_cur_state = False                    


        # Update each light

        if self._low_beam == True :
            self.fit_light(world, position, angle, car_coords, self.low_beam_image )

        if self._high_beam == True :
            self.fit_light(world, position, angle, car_coords, self.high_beam_image ) 

        if self.blink_left_cur_state == True :
            self.fit_light(world, position, angle, car_coords, self.blink_left_image )

        if self.blink_right_cur_state == True :
            self.fit_light(world, position, angle, car_coords, self.blink_right_image )

        if( (self._low_beam == False) and (self._high_beam == False) and (self.blink_left_cur_state == False) and (self.blink_right_cur_state == False) ):
            self.fit_light(world, position, angle, car_coords, self.nolights_image )            


        # TODO

        pass






