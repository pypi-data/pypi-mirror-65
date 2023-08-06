#! /usr/bin/env python
__author__ = ["", ""]
__copyright__ = "Copyright 2019, CPE Lyon"
__credits__ = ["Raphael Leber"]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "Template"

from math import sin, radians, degrees, pi, sqrt, atan
from pygame.math import Vector2
from pygame import time
import logging


class DrivingSystem():
    """ Manage Thottle control, Barking, Steering, and automatic gear box """

    GEAR_CHANGE = 2600
    GEAR_CHANGE_DELTA = 600
    N_GEAR = 1000
    MAX_GEARS = 5
    GEAR_TAB = (0, 0, 2000, 6600, 7200+6600, 9800+7200+6600)
    MAX_MOTOR_SPEED = 6000

    def __init__(self, x, y, angle):
        self.init_x = x
        self.init_y = y
        self.init_angle = angle
        self.__throttle_percent = 0
        self.__brake_percent = 0
        self.__steering_percent = 0 # positive and negative

        self._motor_speed = self.N_GEAR
        self._gear = 0
        self._car_speed = 0
        self._steering_angle = 0

        self.clock = time.Clock()
        self.ticks = 60
        self.dt = 0.0

        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = 2
        self.max_steering_angle = 40
        self.max_car_speed = 10

        self.steering_wheel = 0
        #self.gear = 0
        self.rpm_counter = 0   



        # self.__throttle_percent = 100

    def reset(self):
        self.__throttle_percent = 0
        self.__brake_percent = 0
        self.__steering_percent = 0 # positive and negative

        self._motor_speed = self.N_GEAR
        self._gear = 0
        self._car_speed = 0
        self._steering_angle = 0

        self.dt = 0.0

        self.position = Vector2(self.init_x, self.init_y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = self.init_angle

        self.steering_wheel = 0
        self.rpm_counter = 0           



    ##############################################################################
    # Inputs from the vehicule user/AI
    ##############################################################################

    @property
    def throttle(self):
        """Getter to return throttle percentage"""
        return self.__throttle_percent

    @throttle.setter
    def throttle(self, pedal_percent):
        """Setter to set throttle percentage"""
        if(pedal_percent > 100 or pedal_percent < 0) : 
            raise ValueError("pedal_percent allowed values are between 0 and 100")       
        self.__throttle_percent = pedal_percent


    @property
    def brake(self):
        """Getter to return brake percentage"""
        return self.__brake_percent

    @brake.setter
    def brake(self, pedal_percent):
        """Setter to set brake percentage"""
        if(pedal_percent > 100 or pedal_percent < 0) : 
            raise ValueError("pedal_percent allowed values are between 0 and 100")           
        self.__brake_percent = pedal_percent        
    

    @property
    def steering(self):
        """Getter to return steering percentage"""
        return self.__steering_percent

    @steering.setter
    def steering(self, steering_wheel_percent):
        """Setter to set steering percentage"""
        if(steering_wheel_percent > 100 or steering_wheel_percent < -100) : 
            raise ValueError("pedal_percent allowed values are between -100 and 100")           
        self.__steering_percent = steering_wheel_percent      


    ##############################################################################
    # Outputs for the vehicule user/AI
    ##############################################################################

    @property
    def motor_speed(self):
        """Getter to return motor speed"""
        return self._motor_speed       

    @property
    def gear(self):
        """Getter to return gear"""
        return self._gear     

    @property
    def car_speed(self):
        """Getter to return car speed"""
        return self._car_speed     

    @property
    def steering_angle(self):
        """Getter to return steering angle"""
        return self._steering_angle                             


    ##############################################################################
    # Process vehicule cinematics
    ##############################################################################

    def update(self):
        """Update motor_speed, gears, car_speed, steering_angle"""

        self.dt = self.clock.get_time() / 1000


        self._motor_speed = min(self._motor_speed + self.__throttle_percent  * 10 * self.dt, self.MAX_MOTOR_SPEED)
        self._motor_speed = max (0, self._motor_speed - (self.__brake_percent * 60 + 10) * self.dt)

        if (self._motor_speed > (self.GEAR_CHANGE + self.GEAR_CHANGE_DELTA) or self._gear == 0) and self.__throttle_percent > self.__brake_percent :
            if self._gear < self.MAX_GEARS :
                self._gear += 1
                self._motor_speed = max(self._motor_speed-self.GEAR_CHANGE, 0)

        elif self._motor_speed < (self.GEAR_CHANGE - self.GEAR_CHANGE_DELTA) and self.__throttle_percent <= self.__brake_percent :
            if self._gear > 0:
                self._gear -= 1
                self._motor_speed = self._motor_speed + self.GEAR_CHANGE


        self._car_speed = ( self._motor_speed * self._gear + self.GEAR_TAB[self._gear] ) * 0.004

        self.velocity.xy = (self._car_speed *0.1, 0)


        self._steering_angle = self.__steering_percent * self.dt
        self._steering_angle = max(-self.max_steering_angle, min(self._steering_angle, self.max_steering_angle))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0        

        self.position += self.velocity.rotate(-self.angle) * self.dt
        self.angle += degrees(angular_velocity) * self.dt            

        logging.info("motor_speed: %.3f \t gear: %d \t car_speed: %.3f" % (self._motor_speed, self._gear, self._car_speed) )

        
        self.clock.tick(self.ticks)

    

