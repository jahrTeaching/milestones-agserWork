# Common configuration class.



from functools import reduce



class ConfigItem:
    """Configuration item"""

    def __init__(self, ty) -> None:
        self.val = ty()

    def value(self):
        return self.val

    def tagint(self, name: str, ind, msg: str, ty):
        self.name = name
        self.ind = ind
        self.msg = msg
        self.ty = ty
        self.tag = "int"

    def tagstr(self, name: str, ind, msg: str, ty):
        self.name = name
        self.ind = ind
        self.msg = msg
        self.ty = ty
        self.tag = "str"

    def checkint(self, check: int):
        return (self.tag == "int") and (self.ind == check)

    def checkstr(self, check: str):
        return (self.tag == "str") and ((self.ind == check) or (self.ind == check.upper()) or (self.ind == check.lower()))

    def named(self, name: str):
        return self.name == name

    def display(self) -> str:
        return f"  [{self.ind}] {self.msg}\n"

    def edit(self):
        if self.ty == float:
            self.efloat()
        elif self.ty == int:
            self.eint()
        elif self.ty == bool:
            self.ebool()
        else:
            print(f"[ERROR] Configuration items of type {self.ty} are not supported")

    def ebool(self):
        msg = f"Enter the new value for {self.name} [Y/N]: "

        string = input(msg)

        if string in ["Y", "y"]:
            self.val = True
        elif string in ["N", "n"]:
            self.val = False
        else:
            print(f"[ERROR] Could not parse string '{string}' as boolean (not in ['Y', 'y', 'N', 'n'])")

    def efloat(self):
        msg = f"Enter the new value for {self.name} [float]: "

        string = input(msg)

        try:
            self.val = float(string)
        except Exception as e:
            print(f"[ERROR] Could not parse string '{string}' as float: [Error] {e}")

    def eint(self):
        msg = f"Enter the new value for {self.name} [int]: "

        string = input(msg)

        if string.isnumeric():
            try:
                self.val = int(string)
            except Exception as e:
                print(f"[ERROR] Could not parse string '{string}' as integer: [Error] {e}")
        else:
            print(f"[ERROR] Cannot parse non integer string '{string}' as integer")



class Config:
    """Configuration structure containing the parameters for the configuration of a milestone"""

    def __init__(self) -> None:
        self.items = []

    def getitem(self, name):
        return list( filter(lambda item: item.named(name), self.items) )[0]

    def additem(self, name, ind, msg, ty):
        item = ConfigItem(ty)

        if type(ind) == str:
            item.tagstr(name, ind, msg, ty)
        elif type(ind) == int:
            item.tagint(name, ind, msg, ty)
        else:
            print(f"[ERROR] Indicator not supported: Type = {type(ind)}")
            return

        self.items.append( item )

    def edit(self):
        # Build the message.
        message = reduce( lambda x, y: x + y, map( ConfigItem.display, self.items ) )
        message += "  [B] Back\n>> "

        while True:
            # Read the input
            string = input(message)

            # Check for return
            if string in ["B", "b"]:
                return

            if not string.isnumeric():
                selected = list( filter( lambda item: item.checkstr(string), self.items ) )

                if selected is not None and len(selected) > 0:
                    selected[0].edit()
                else:
                    print(f"[ERROR] The string {string} does not correspond to any item")
            else:
                try:
                    index = int(string)
                except:
                    print(f"[ERROR] The string {string} could not be converted to an index")
                
                selected = list( filter(lambda item: item.checkint(index), self.items) )

                if selected is not None and len(selected) > 0:
                    selected[0].edit()
                else:
                    print(f"[ERROR] The string {string} does not correspond to any item")




if __name__ == "__main__":
    print("Testing configuration editor\n")

    config = Config()

    config.additem("test1", 1, "Item 1 in test configuration", int)
    config.additem("test2", "A", "Item 2 in test configuration", float)

    config.edit()

    test1 = config.getitem("test1")
    test2 = config.getitem("test2")

    print( f"Variable test1 is {test1}" )
    print( f"Variable test2 is {test2}" )
