# Menu selector of milestone 3



from common.config import Config
from common.menu import Menu
from . import items



def menu():
    # Build the configuration.
    config = Config()

    config.additem("start", 1, "Start time",                          float)
    config.additem("end",   2, "End time",                            float)
    config.additem("steps", 3, "Number of steps in the time interval",  int)
    config.additem("X0",    4, "Initial X coordinate",                float)
    config.additem("Y0",    5, "Initial Y coordinate",                float)
    config.additem("VX0",   6, "Initial X velocity",                  float)
    config.additem("VY0",   7, "Initial Y velocity",                  float)
    config.additem("order", 8, "Order of the system",                   int)

    # Build the menu.
    menu = Menu()

    menu.setconfig(config)

    menu.additem("error", 1, "Calculate the Richardson Error", items.richardson)
    menu.additem("conv",  2, "Calculate Convergence rates",  items.convergencia)

    menu.menu()
