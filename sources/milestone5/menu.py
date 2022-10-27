# Menu selector of milestone 5



from common.config import Config
from common.menu import Menu
from common.physics import NBody
#from . import items



def menu():
    # Build the configuration.
    config = Config()

    config.additem("num",   1, "Number of bodies",                      int)
    config.additem("steps", 2, "Number of steps",                       int)
    config.additem("dt",    3, "Time interval between steps",         float)

    # Build the menu.
    menu = Menu()

    menu.setconfig(config)

    menu.additem("nbody", 1, "N-Body problem", NBody)

    menu.menu()
