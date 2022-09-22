# Orbit computation using Range-Kutta Order 4 integration.

import matplotlib.pyplot as plt
import numpy as np
import math



def compute():
    # Create default values
    dt = 1.0
    x, y = 8000000.0, 0
    vx, vy = 0.0, 7072.0

    # Gravitational parameter
    nu = (6.67 * (10.0 ** -11.0)) * (5.0 * (10.0 ** 24.0))

    #List to collect the data
    points = [[x, y]]

    #Start looping
    for i in range(0, 10000):
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


def step_(nu, x, y, vx, vy, dt):
    # Get K1 coefficient.
    k1x, k1y = force(nu, x, y)
    k1x = vx + (k1x * dt)
    k1y = vy + (k1y * dt)

    # Update X, Y, VX, VY and get K2 coefficient.
    k2x, k2y = force(nu, x + (k1x * dt / 2.0), y + (k1y * dt / 2.0))
    k2x = vx + (k2x * dt / 2.0)
    k2y = vy + (k2y * dt / 2.0)

    # Update X, Y, VX, VY and get K3 coefficient.
    k3x, k3y = force(nu, x + (k2x * dt / 2.0), y + (k2y * dt / 2.0))
    k3x = vx + (k3x * dt / 2.0)
    k3y = vy + (k3y * dt / 2.0)

    # Update X, Y, VX, VY and get K4 coefficient.
    k4x, k4y = force(nu, x + (k3x * dt), y + (k3y * dt))
    k4x = vx + (k4x * dt)
    k4y = vy + (k4y * dt)

    return x + ((k1x + k4x + (2.0 * (k2x + k3x))) * dt / 6.0), y + ((k1y + k4y + (2.0 * (k2y + k3y))) * dt / 6.0)



def force(nu, x, y):
    distance = math.sqrt((x ** 2) + (y ** 2)) ** 3.0
    factor = nu / distance
    return -factor * x, -factor * y


if __name__ == "__main__":
    compute()