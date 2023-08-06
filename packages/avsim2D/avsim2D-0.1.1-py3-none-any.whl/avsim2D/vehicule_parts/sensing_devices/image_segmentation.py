#! /usr/bin/env python
__author__ = ["", ""]
__copyright__ = "Copyright 2019, CPE Lyon"
__credits__ = ["Baptiste Brejon, Marion Deshayes"]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "Template"

import pygame
from math import sin,pi, cos, atan

class RadarDetectSprite(pygame.sprite.Sprite):
    """Radar sprite object

    Definition of the sensor sprite
    Attributs
    ----------
    rect : pygame.Rect
    image : pygame.Surface
    """
    def __init__(self,x,y):
        """Initialisation of Radar sprite object

        initialisation of the sensor sprite

        Parameters
        ----------
        x : int
            x-axis position of the sprite rectangle
        y : int
            y-axis position of the sprite rectangle
        """
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 1, 1)
        self.image = pygame.Surface((1,1))


class SementicWeight():

    def __init__(self):
        #self.left
        #self.middle_left
        #self.middle_right
        #self.right
        self.road = 0.0
        self.stop_mark = 0.0
        self.yield_mark = 0.0
        self.crossing_mark = 0.0
        self.car_park = 0.0
        self.not_allowed = 0.0
        self.people = 0.0
        self.path = 0.0


    def update(self, world, rectangle, dist  ):
        
        if world.layers_map.is_layer(rectangle.rect.x, rectangle.rect.y, "road"):
            weight = (32 - dist) / 32
            self.road = min(255, self.road + weight )

        if world.layers_map.is_layer(rectangle.rect.x, rectangle.rect.y, "stop"):
            weight = (32 - dist) / 32
            self.stop_mark = min(255, self.stop_mark + weight )

        if world.layers_map.is_layer(rectangle.rect.x, rectangle.rect.y, "yield"):
            weight = (32 - dist) / 32
            self.yield_mark = min(255, self.yield_mark + weight )
            
        if world.layers_map.is_layer(rectangle.rect.x, rectangle.rect.y, "crossing"):
            weight = (32 - dist) / 32
            self.crossing_mark = min(255, self.crossing_mark + weight )       

        if world.layers_map.is_layer(rectangle.rect.x, rectangle.rect.y, "car_park"):
            weight = (32 - dist) / 32
            self.car_park = min(255, self.car_park + weight )      


        """
        if world.layers_map.is_layer(rectangle.rect.x, rectangle.rect.y, "TODO"):
            weight = (32 - dist) / 32
            self.not_allowed = min(255, self.not_allowed + int(weight) ) 

        if world.layers_map.is_layer(rectangle.rect.x, rectangle.rect.y, "TODO"):
            weight = (32 - dist) / 32
            self.people = min(255, self.people + int(weight) )                                          
        """

        if world.layers_map.is_layer(rectangle.rect.x, rectangle.rect.y, "path"):
            weight = (32 - dist) / 32
            self.path = min(255, self.path + weight )      

    
        


class ImageSegmentation():
    """ Manage camera high level information """


    def __init__(self):
        self.sensor_sprite = RadarDetectSprite(0, 0)
        self.sensor_group = pygame.sprite.Group()

        self.sensor_range = 15
        self.flag_human_detect = False
        self.danger_zone = 5        

        self.draw_camera_field = False

        self.semantic_sensor = {}

        self.zone = ("full_left", "left", "middle_left", "middle_right", "right", "full_right")

        for sub in self.zone:
            self.semantic_sensor[sub] = SementicWeight()


    def update(self, world, obstacles, screen, posvoiture, car_angle, human):
        """Simulated a sensor detection

        This function simulated a sensor detection by using pygame.sprite.groupcollide and pygame.sprite.spritecollide features.
        It will return a 2-length list message with the appropriate behavior of the car, depends of the detection.

        Parameters
        ----------
        obstacles : pygame.sprite.Group
            Group of sprites declared as obstacles
        screen : pygame.display
            The current window of the simulation
        posvoiture : Vector2(x, y)
            A vector which contains the current x and y coordinates of the car
        car_angle : float
            The current value of the car orientation
        human : pygame.sprite
            the human sprite

        Returns
        -------
        semantic_sensor
        """

        posx = posvoiture[0]
        posy = posvoiture[1]
        point_central = (posx, posy)


        #semantic_sensor = {}
        
        for sub in self.zone:
            self.semantic_sensor[sub] = SementicWeight()

        max_angle = 180

        #This this the angle in front of the car we would like to scoot.
        detect_angle = 27        


        # The sensor position, calculation to always put it in the front of the car
        sensor_pos = (posx + 17*cos((car_angle%360)*pi/180), posy - 17*sin((car_angle%360)*pi/180))

        #Test collides with different groups
        collision_obstacle = pygame.sprite.groupcollide(self.sensor_group, obstacles, False, False)
        collision_humain = pygame.sprite.spritecollide(human,self.sensor_group, False)

        #If collide with a human
        if len(list(collision_humain)) != 0:
            #Calculation of the absolute distance to the human, and return brake if it's to close
            abs_distance_human = ((human.rect.x - posx) ** 2 + (human.rect.y - posy) ** 2) ** (1 / 2)

            if abs_distance_human  <= self.sensor_range + 2 :
                msg_speed = "brake"
                self.flag_human_detect = True

        #If sensor collides with an obstacle
        if len(list(collision_obstacle.keys())) != 0:

            for value in list(collision_obstacle.values()):
                for rectangle in value:

                    #Calculation of the absolute distance between the sensor and the obstacle
                    abs_dist_sensor_obstacle = ( (rectangle.rect.x - sensor_pos[0])**2 + (rectangle.rect.y - sensor_pos[1])**2) **(1/2)

                    #Under this distance threshold, the car should steer to avoid obstacle
                    threshold_steering = ( (rectangle.rect.x - posx)**2 + (rectangle.rect.y - posy)**2) **(1/2)

                    #Under this distance threshold, the car should slow to avoid obstacle
                    threshold_brake = threshold_steering - 2

                    norme_point_central = ((rectangle.rect.x - point_central[0]) ** 2 + (
                    rectangle.rect.y - point_central[1]) ** 2) ** (1 / 2)





                    #If the obstacle is in the car front area
                    if abs_dist_sensor_obstacle <= self.sensor_range :
                        
                        #Calculation of the slope between the obstacle and the car
                        if (rectangle.rect.x - posx) != 0 :
                            slope = (rectangle.rect.y - posy)/(rectangle.rect.x - posx)
                            slope_angle = atan(slope)*180/pi
                        else :
                            slope_angle = 1000



                        # Determination of the obstacle's side. Here if it is on the MIDDLE_RIGHT
                        if  (slope_angle + car_angle )%max_angle < detect_angle/3 :

                            #Right = red color
                            color = pygame.Color(200, 0, 0)
                                
                            self.semantic_sensor["middle_right"].update( world, rectangle, abs_dist_sensor_obstacle)


                        # Determination of the obstacle's side. Here if it is on the MIDDLE_LEFT
                        elif (slope_angle + car_angle) % max_angle > max_angle - detect_angle/3:

                            #Left = pink color
                            color = pygame.Color(200, 0, 200)

                            self.semantic_sensor["middle_left"].update( world, rectangle, abs_dist_sensor_obstacle)

                        # Determination of the obstacle's side. Here if it is on the LEFT
                        elif (slope_angle + car_angle) % max_angle > max_angle - detect_angle:

                            #Left = pink color
                            color = pygame.Color(200, 0, 100)

                            self.semantic_sensor["left"].update( world, rectangle, abs_dist_sensor_obstacle)

                        # Determination of the obstacle's side. Here if it is on the FULL_LEFT
                        elif (slope_angle + car_angle) % max_angle > max_angle - detect_angle*2:

                            #Left = pink color
                            color = pygame.Color(200, 0, 50)     

                            self.semantic_sensor["full_left"].update( world, rectangle, abs_dist_sensor_obstacle)                          

                        # Determination of the obstacle's side. Here if it is on the RIGHT
                        elif (slope_angle + car_angle )%max_angle < detect_angle :

                            #Right = red color
                            color = pygame.Color(100, 0, 0)

                            self.semantic_sensor["right"].update( world, rectangle, abs_dist_sensor_obstacle)          

                        # Determination of the obstacle's side. Here if it is on the FULL_RIGHT
                        elif (slope_angle + car_angle )%max_angle < detect_angle*2 :

                            #Right = red color
                            color = pygame.Color(50, 0, 0)

                            self.semantic_sensor["full_right"].update( world, rectangle, abs_dist_sensor_obstacle)    

                        else :
                            color = pygame.Color(200, 200, 0)

                        if "crossing" in world.layers_map.get_layers(rectangle.rect.x, rectangle.rect.y):
                            color = pygame.Color(255, 255, 255)

                        if(self.draw_camera_field):

                            #Drawing of the obstacle to see the detection on the screen
                            rect_filled = pygame.Surface((8,8))
                            pygame.draw.rect(rect_filled, color, rect_filled.get_rect())
                            screen.blit(rect_filled, (rectangle.rect.x * 8, rectangle.rect.y * 8))




        return self.semantic_sensor
