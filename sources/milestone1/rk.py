# Orbit computation using Range-Kutta Order 4 integration.

import matplotlib.pyplot as plt
import numpy as np
import math



def compute(start, dt, steps):
    # Create default values
    x, y = start[0], start[1]
    vx, vy = start[2], start[3]

    # Gravitational parameter
    nu = 1.0

    #List to collect the data
    points = [[x, y]]

    #Start looping
    for i in range(0, steps):
        #RK4 step.
        dvx, dvy = step(nu, x, y, vx, vy, dt)

        #Update velocity.
        vx += dvx * dt
        vy += dvy * dt

        # Update points.
        x += vx * dt
        y += vy * dt

        #Store the points
        points.append([x, y])

    # Display the points
    fig, ax = plt.subplots()
    ax.plot([p[0] for p in points], [p[1] for p in points])

    ax.set(title='Runge-Kutta O(4) orbit')

    plt.show()


def step(nu, x, y, vx, vy, dt):
    # Get K1 coefficient.
    a1x, a1y = force(nu, x, y)

    # Get K2 coefficient.
    a2x, a2y = force(nu, x + (vx + (a1x * dt / 2.0)), y + (vy + (a1y * dt / 2.0)))

    # Get K3 coefficient.
    a3x, a3y = force(nu, x + (vx + (a2x * dt / 2.0)), y + (vy + (a2y * dt / 2.0)))

    # Get K4 coefficient.
    a4x, a4y = force(nu, x + (vx + (a3x * dt)), y + (vy + (a3y * dt)))

    return (a1x + a4x + 2.0 * (a2x + a3x)) * dt / 6.0, (a1y + a4y + 2.0 * (a2y + a3y)) * dt / 6.0


def force(nu, x, y):
    distance = math.sqrt((x ** 2) + (y ** 2)) ** 3.0
    factor = nu / distance
    return -factor * x, -factor * y


if __name__ == "__main__":
    compute([1.0, 0.0, 0.0, 1.0], 0.001, 10000)