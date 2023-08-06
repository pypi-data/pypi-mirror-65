#! /usr/bin/env python
__author__ = ["", ""]
__copyright__ = "Copyright 2019, CPE Lyon"
__credits__ = ["Raphael Leber"]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "Template"

from .sensing_devices import Ranger
from .sensing_devices import ImageSegmentation


class Sensing():
    """ Manage vehicule sensor """

    def __init__(self):
        self.image_segmentation = ImageSegmentation()
        self.ranger = Ranger()

    def update(self, world, obstacles,screen, posvoiture, car_angle, human):

        self.image_segmentation.update(world, obstacles,screen, posvoiture, car_angle, human)
        self.ranger.update()

        # TODO

        pass
