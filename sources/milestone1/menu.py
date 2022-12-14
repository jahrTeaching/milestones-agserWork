# Menu selector of milestone 1


from . import common

from . import euler as eu
from . import cn
from . import rk

def menu():
    # Default configuration.
    config = common.Config()

    print(f"Config struct {config}")

    # Build the list of methods.
    methods = []

    methods.append(("Euler",            eu.compute))
    methods.append(("Range-Kutta O(4)", rk.compute))
    methods.append(("Crank-Nicolson",   cn.compute))

    # Build the input message.
    message = "Select orbit method:\n"

    for i in range(0, len(methods)):
        message += f"  [{i+1}] {methods[i][0]}\n"

    message += "  [B] Back\n\n>> "

    while True:
        s = input(message)

        if s == "b" or s == "B":
            return

        if s in ["E", "e"]:
            config.edit()
            continue

        if not s.isnumeric():
            print(f"Input not recognized: '{string}'")
            continue

        select = int(s)

        if select < 1:
            print(f"Minimum index is 1")
            continue

        methods[select-1][1](config.start, config.dt, config.steps)


if __name__ == "__main__":
    menu()