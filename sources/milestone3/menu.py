# Menu selector of milestone 3



from common.menu import Menu


def empty():
    pass

def menu():
    # Build the menu.
    menu = Menu()

    menu.additem("empty", 0, "Empty menu item", empty)

    menu.menu()
