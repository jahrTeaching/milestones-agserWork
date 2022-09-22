# Menu selection of milestone


from milestone1 import menu as m1



if __name__ == "__main__":
    while True:
        string = input("Select milestone:\n  [1] Milestone 1: Simple orbit methods\n  [Q] Quit\n\n>> ")

        if string == "q" or string == "Q":
            break

        if not string.isnumeric():
            print(f"Input not recognized: '{string}'")
            continue

        select = int(string)

        if select == 1:
            m1.menu()
