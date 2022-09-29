# Menu selector of milestone 2


from . import common
from . import items


def empty():
    pass

def menu():
    # Default configuration.
    config = common.Config()

    # Build the list of methods.
    methods = []
    methods.append( ("Euler",          items.eu) )
    methods.append( ("Inverse Euler",  items.ie) )
    methods.append( ("Runge-Kutta 4",  items.rk) )
    methods.append( ("Crank-Nicolson", items.cn) )


    # Build the input message.
    message = "Select orbit method:\n"

    for i in range(0, len(methods)):
        message += f"  [{i+1}] {methods[i][0]}\n"

    message += "  [E] Edit configuration\n  [J] Display the energy plot of all schemes\n  [O] Display the orbit plot of all schemes\n  [B] Back\n\n>> "

    while True:
        s = input(message)

        if s in ["B", "b"]:
            return

        if s in ["E", "e"]:
            config.edit()
            continue

        if s in ["O", "o"]:
            items.orbits(config)
            continue

        if s in ["J", "j"]:
            items.energies(config)
            continue

        if not s.isnumeric():
            print(f"Input not recognized: '{string}'")
            continue

        select = int(s)

        if select < 1:
            print(f"Minimum index is 1")
            continue

        methods[select-1][1]( config )
