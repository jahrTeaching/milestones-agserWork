# Common abstractions for Milestone 2.

from numpy import array


class Config:
    """Configuration structure containing the necessary parameters for this milestone"""
    def __init__(self):
        self.steps = 10000
        self.tmax = 50
        self.dt = 10.0
        self.start = [1.0, 0.0, 0.0, 1.0]

    def edit(self):

        message = "Edit Configuration:\n  [1] Number of steps\n  [2] Time delta\n  [4] Starting conditions\n  [B] Back\n\n>> "

        while True:
            string = input(message)

            if string in ["B", "b"]:
                return

            if not string.isnumeric():
                print("Invalid input")
                continue

            select = int(string)

            if select == 1:
                self.editsteps()
            elif select == 2:
                self.editdelta()
            elif select == 3:
                self.edittmax()
            elif select == 4:
                self.editstart()
            else:
                print("Unrecognized input")

    def editsteps(self):
        string = input("Entrer the desired number of steps")

        if not string.isnumeric():
            print("Not a number")
            return

        self.steps = int(string)

    def editdelta(self):
        string = input("Enter the desired time delta")

        if not string.isnumeric():
            print("Not a number")
            return

        self.delta = float(string)

    def edittmax(self):
        string = input("Enter maximum time")

        if not string.isnumeric():
            print("Not a number")
            return

        self.tmax = float(string)

    def editstart(self):
        message = "Edit Configuration:\n  [1] Position X\n  [2] Position Y\n  [3] Velocity X\n [4] Velocity Y\n  [B] Back\n\n>> "

        while True:
            string = input(message)

            if string in ["B", "b"]:
                return
                
            if not string.isnumeric():
                print("Not a number")
                continue

            select = int(string)
            
            if select > 4 or select < 1:
                print("Invalid input")
                continue
                
            substring = input("Value")

            if not substring.isnumeric():
                print("Not a number")
                continue

            self.start[i-1] = float(substring)
