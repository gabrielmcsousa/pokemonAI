# from pokecenter import Pokecenter
# from pokestore import Pokestore
# from trainer import Trainer
# from pokemon import Pokemon
import numpy as np

class Map(object):

    def __init__(self):
        self.generateGrassMap()


    """CREATE MAP FILE FILLED WITH GRASS"""
    def generateGrassMap(self):
        f = open("newMap.txt", "a")
        for a in range(0,42):
            for b in range(0,41):
                f.write("G")
                f.write(" ")
            f.write("G")
            f.write("\n")
        f.close()

map = Map()