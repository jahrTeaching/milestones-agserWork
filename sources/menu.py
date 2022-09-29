# Menu selection of milestone


from milestone1 import menu as m1
from milestone2 import menu as m2
from milestone3 import menu as m3
from milestone4 import menu as m4
from milestone5 import menu as m5
from milestone6 import menu as m6



if __name__ == "__main__":
    # Build the list of milestones.
    milestones = []

    milestones.append(("Simple orbit methods",   m1.menu))
    milestones.append(("Composed orbit methods", m2.menu))
    milestones.append(("", m3.menu))
    milestones.append(("", m4.menu))
    milestones.append(("", m5.menu))
    milestones.append(("", m6.menu))

    # Build the input message.
    message = "Select milestone:\n"

    for i in range(0, len(milestones)):
        message += f"  [{i+1}] Milestone {i+1}: {milestones[i][0]}\n"

    message += "  [Q] Quit\n\n>> "
    
    while True:
        string = input(message)

        if string == "q" or string == "Q":
            break

        if not string.isnumeric():
            print(f"Input not recognized: '{string}'")
            continue

        select = int(string)

        if select < 1:
            print("Minimum index is 1")
            continue

        milestones[select-1][1]()
