# Orbit computation using Crank-Nicholson integration.

import matplotlib.pyplot as plt
import numpy as np
import math



def compute():
    # Create default values
    dt = 1.0
    x, y = 8000000.0, 0
    vx, vy = 0.0, 8000.0

    # Gravitational parameter
    nu = (6.67 * (10.0 ** -11.0)) * (5.0 * (10.0 ** 24.0))

    #List to collect the data
    points = [[x, y]]

    #Start looping
    for i in range(0, 25000):
        # Calculate force in step n.
        dvxa, dvya = force(nu, x, y)

        #Calculate the new position
        x += vx * dt
        y += vy * dt

        # Calculate force in step n+1.
        dvxb, dvyb = force(nu, x, y)
        vx += (dvxa + dvxb) * dt / 2.0
        vy += (dvya + dvyb) * dt / 2.0

        #Store the points
        points.append([x, y])

    # Display the points
    fig, ax = plt.subplots()
    ax.plot([p[0] for p in points], [p[1] for p in points])

    ax.set(title='Crank-Nicholson orbit')

    plt.show()



def force(nu, x, y):
    distance = math.sqrt((x ** 2) + (y ** 2)) ** 3.0
    factor = nu / distance
    return -factor * x, -factor * y


if __name__ == "__main__":
    compute()