# Common menu class.



from functools import reduce
from typing import Callable



class MenuItem:
    """Configuration item"""

    def tagint(self, name: str, ind, msg: str, fun: Callable):
        self.name = name
        self.ind = ind
        self.msg = msg
        self.fun = fun
        self.tag = "int"

    def tagstr(self, name: str, ind, msg: str, fun: Callable):
        self.name = name
        self.ind = ind
        self.msg = msg
        self.fun = fun
        self.tag = "str"

    def checkint(self, check: int):
        return (self.tag == "int") and (self.ind == check)

    def checkstr(self, check: str):
        return (self.tag == "str") and ((self.ind == check) or (self.ind == check.upper()) or (self.ind == check.lower()))

    def named(self, name: str):
        return self.name == name

    def display(self) -> str:
        return f"  [{self.ind}] {self.msg}\n"

    def run(self, config=None):
        if config is None:
            self.fun()
        else:
            self.fun(config)


class Menu:
    """Menu structure containing the parameters for the menu selection of a milestone"""

    def __init__(self) -> None:
        self.items = []
        self.config = None

    def setconfig(self, config):
        self.config = config

    def getitem(self, name):
        return filter(lambda item: item.named(name), self.items)

    def additem(self, name, ind, msg, fun: Callable):
        item = MenuItem()

        if type(ind) == str:
            item.tagstr(name, ind, msg, fun)
        elif type(ind) == int:
            item.tagint(name, ind, msg, fun)
        else:
            print(f"[ERROR] Indicator not supported: Type = {type(ind)}")
            return

        self.items.append( item )

    def menu(self):
        # Build the message.
        message = reduce( lambda x, y: x + y, map( MenuItem.display, self.items ) )

        if self.config is not None:
            message += "\n  [E] Edit configuration\n"

        message += "\n  [B] Back\n>> "

        while True:
            # Read the input
            string = input(message)

            # Check for return and configuration edit
            if string in ["B", "b"]:
                return

            if string in ["E", "e"] and self.config is not None:
                self.config.edit()
                continue

            if not string.isnumeric():
                selected = list( filter( lambda item: item.checkstr(string), self.items ) )

                if selected is not None and len(selected) > 0:
                    selected[0].run(self.config)
                else:
                    print(f"[ERROR] The string {string} does not correspond to any item")
            else:
                try:
                    index = int(string)
                except:
                    print(f"[ERROR] The string {string} could not be converted to an index")
                
                selected = list( filter(lambda item: item.checkint(index), self.items) )

                if selected is not None and len(selected) > 0:
                    selected[0].run(self.config)
                else:
                    print(f"[ERROR] The string {string} does not correspond to any item")



if __name__ == "__main__":
    from config import Config

    jaja = lambda x: print("jaja")
    hehe = lambda x: print("hehe")

    print("Testing menu editor\n")

    config = Config()

    config.additem("test1", 1, "Item 1 in test configuration", int)
    config.additem("test2", "A", "Item 2 in test configuration", float)

    menu = Menu()

    menu.additem("item1", 1, "Item 1 in menu", jaja)
    menu.additem("item2", "a", "Item 2 in menu", hehe)

    menu.setconfig(config)

    menu.menu()
