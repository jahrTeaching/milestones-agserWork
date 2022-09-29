import matplotlib.pyplot as plt
import numpy as np
import math


def compute(start, dt: float, steps: float):
    # Create default values
    x, y = start[0], start[1]
    vx, vy = start[2], start[3]

    # Gravitational parameter
    #nu = (6.67 * (10.0 ** -11.0)) * (5.0 * (10.0 ** 24.0))
    #nu = (6.67 * (10.0 ** -11.0)) * (1000000)
    nu = 1.0

    #List to collect the data
    points = [[x, y]]

    #Start looping
    for i in range(0, steps):
        print(f"Step {i}:\n   X,  Y: [{x}, {y}]\n  VX, VY: [{vx}, {vy}]")
    
        #Calculate the new position
        x += vx * dt
        y += vy * dt

        # Calculate the new velocity
        dvx, dvy = force(nu, x, y)
        vx += dvx * dt
        vy += dvy * dt

        #Store the points
        points.append([x, y])

    # Display the points
    fig, ax = plt.subplots()
    ax.plot([p[0] for p in points], [p[1] for p in points])

    ax.set(title='Euler orbit')

    plt.show()

def force(nu, x, y):
    distance = math.sqrt((x ** 2) + (y ** 2)) ** 3.0
    factor = nu / distance
    return -factor * x, -factor * y

if __name__ == "__main__":
    compute([1.0, 0.0, 0.0, 1.0], 0.01, 10000)