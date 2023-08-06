#! /usr/bin/env python
# coding=utf-8

__author__ = ["Marion Deshayes", "Baptiste BREJON", "Raphaël Leber"]
__copyright__ = "Copyright 2020, CPE Lyon"
__credits__ = [" "]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "draft"


import pygame
import pytmx

import os

from .human import Human


class Tile(pygame.sprite.Sprite):
    """Tile object
    each 8px square tile of the map should be associated to a sprite for ease the collide detection
    """

    def __init__(self,x,y,image):
        """Initialisation of a Tile sprite object

        initialisation of the tile sprite.
        We use it on each 8px square from layers of the map

        Parameters
        ----------
        x : int
            x-axis position of the sprite rectangle
        y : int
            y-axis position of the sprite rectangle
        image : pygame.Surface
            image of the tile
        """
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,1,1)
        self.image = image


class TileCoordLayers():
    """T
    
    """

    def __init__(self, x=0, y=0, layer=None):

        self.x = x
        self.y = y
        self.layers = []
        if layer != None:
            self.add_layer(layer)

    def add_layer(self, layer):
        self.layers.append(layer)


class LayersMap():
    """T
    
    """

    def __init__(self):

        #self.xy = (x, y)
        self.map = {}

    def add_tile(self, tile_coord_layer):
        
        xy = (tile_coord_layer.x, tile_coord_layer.y)
        self.map[xy] = tile_coord_layer.layers

    def get_layers(self, x, y):
        xy = (x, y)
        layers = self.map[xy]
        return layers

    def add_layer(self, x, y, layer):
        xy = (x, y)
        self.map[xy].append(layer)

    def is_layer(self, x, y, layer_name):
        if layer_name in self.get_layers(x, y):
            return True
        return False



class World():
    """World manager
    This class manage the world appearance

    Attributs:
    ---------
    self.width : int
        Width of the screen
    self.height : int
        Height of the screen
    self.screen : pygame.display
        The current screen for the simulation
    self.obstacles : pygame.sprite.Group
        Group of sprites for each 8px square of side walk layer
    self.gameMap : pytmx.load_pygame
        It contains the each layer of the map

    Methods
    -------
    __init__(self)
    init_map(self)
    update_map_back(self)
    update_map_front(self)
    """

    def __init__(self):
        """Initialisation of attributs
        
        This will initialyze attributs of world class
        """

        pygame.init()
        pygame.display.set_caption("avsim2D : Autonomous Vehicle Simulator 2D - with CanBus drive by wire - by Raphaël LEBER")
        self.width = 1280
        self.height = 720

        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "Images/vehicules/car_blue_icon.png")              
        programIcon = pygame.image.load(icon_path)
        pygame.display.set_icon(programIcon)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.obstacles = pygame.sprite.Group()
        self.road = pygame.sprite.Group()
        self.gameMap = None

        self.layers_map = LayersMap()

        self.human = Human(41, 36)

    def init_map(self):
        """Initialisation of the map

        This function will read the .tmx file and display it layer by layer.
        For some layer, layer_side_walk and layer_marking, it will also fill the appropriate group of sprites

        """

        current_dir = os.path.dirname(os.path.abspath(__file__))
        world_path = os.path.join(current_dir, "tiled/CPE_3.tmx")  

        #Load of the .tmx file
        self.gameMap = pytmx.load_pygame(world_path)

        road = self.gameMap.get_layer_by_name("road")

        for i in range(160):
            for j in range(90):
                coordlayers = TileCoordLayers(i, j)
                self.layers_map.add_tile(coordlayers)

        for layer in self.gameMap.visible_layers:
            for x, y, gid, in layer:
                if gid != 0:
                    self.layers_map.add_layer(x, y , layer.name)


        #For each layer of the map, display each 8px square tile
        for layer in self.gameMap.visible_layers:

            for x, y, gid, in layer:
                tile = self.gameMap.get_tile_image_by_gid(gid)
                if(tile != None):
                    self.screen.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))

            pygame.display.update()

            #Fill the obstacle sprites group
            if layer.name == "side_road" or True:
                layer = self.gameMap.get_layer_by_name(layer.name)

                for x, y, image in layer.tiles():
                    tuile = Tile(x,y,image)
                    self.obstacles.add(tuile)

            #Fill the road sprites groupe
            if layer.name == "road" or layer.name == "yield" or layer.name == "stop" or layer.name == "crossing":
                layer = self.gameMap.get_layer_by_name(layer.name)

                for x, y, image in layer.tiles():
                    tuile = Tile(x,y,image)
                    self.road.add(tuile)        

            """
            for x, y, image in layer.tiles():
                tuile = Tile(x,y,image)
                self.road.add(tuile)                                   
            """

    def update_map_back(self):
        """Update of the map background
        In the purpose to create a kind of 2D+ map (depth axis), we update the map in two part,
        one should be display under the car,
        the second should be over the car
        This function update the display of each tile which should be under the car
        """
        # trans="ff00ff"
        for layer in self.gameMap.visible_layers:
            if layer.name != "building_1" and layer.name != "building_2" or layer.name == "labels":
                for x, y, gid, in layer:
                    tile = self.gameMap.get_tile_image_by_gid(gid)
                    if (tile != None):
                        self.screen.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))


    def update_map_front(self):
        """Update of the map foreground
        In the purpose to create a kind of 2D+ map (depth axis), we update the map in two part,
        one should be display under the car,
        the second should be over the car
        This function update the display of each tile which should be over the car
        """
        for layer in self.gameMap.visible_layers:
            if layer.name == "building_1" or layer.name == "building_2" or layer.name == "labels":
                # if layer.name == "layer_side_walk":
                # if pygame.sprite.spritecollideany(rect,layer):
                for x, y, gid, in layer:
                    tile = self.gameMap.get_tile_image_by_gid(gid)
                    if (tile != None):
                        self.screen.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))

    
    def update(self):
        self.human.update(self.screen)

        pass



if __name__ == "__main__":

    world = World()
    #world.update()
    