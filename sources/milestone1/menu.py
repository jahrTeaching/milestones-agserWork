# Menu selector of milestone 1


from . import euler
from . import cn
from . import rk

def menu():
    while True:
        string = input("Select orbit method:\n  [1] Euler\n  [2] Range-Kutta O(4)\n  [3] Crank-Nicholson\n  [4] Back\n\n>> ")

        if not string.isnumeric():
            print(f"Input not recognized: '{string}'")
            continue

        select = int(string)

        if select == 1:
            euler.compute()
        elif select == 2:
            rk.compute()
        elif select == 3:
            cn.compute()
        elif select == 4:
            return
        else:
            print(f"Unrecognized input: '{string}'")
