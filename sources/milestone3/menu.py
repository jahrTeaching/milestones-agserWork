# Menu selector of milestone 3



def empty():
    pass

def menu():
    # Build the list of methods.
    methods = [("Empty", empty)]


    # Build the input message.
    message = "Select orbit method:\n"

    for i in range(0, len(methods)):
        message += f"  [{i+1}] {methods[i][0]}\n"

    message += "  [B] Back\n\n>> "

    while True:
        s = input(message)

        if s == "b" or s == "B":
            return

        if not s.isnumeric():
            print(f"Input not recognized: '{string}'")
            continue

        select = int(s)

        if select < 1:
            print(f"Minimum index is 1")
            continue

        methods[select-1][1]()
