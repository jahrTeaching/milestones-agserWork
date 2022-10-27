# Menu selection of milestone


import common

from common.menu import Menu

from milestone1 import menu as m1
from milestone2 import menu as m2
from milestone3 import menu as m3
from milestone4 import menu as m4
from milestone5 import menu as m5
from milestone6 import menu as m6



if __name__ == "__main__":
    # Build the main menu
    menu = Menu()

    menu.additem("milestone1", 1, "M1 - Simple orbit methods",      m1.menu)
    menu.additem("milestone2", 2, "M2 - Composed orbit methods",    m2.menu)
    menu.additem("milestone3", 3, "M3 - Richardson relative error", m3.menu)
    menu.additem("milestone4", 4, "M4 - Placeholder",               m4.menu)
    menu.additem("milestone5", 5, "M5 - N-Body problem",            m5.menu)

    menu.menu()
