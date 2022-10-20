# Orbit computation using Crank-Nicholson integration.

import matplotlib.pyplot as plt
from numpy import array, zeros
from scipy.optimize import fsolve
import math



def compute(start, dt, steps):
    # Create default values
    U = zeros((4, steps))
    U[:,0] = array(start)
    F = zeros(4)

    # Gravitational parameter
    nu = 3.986e14

    # Start looping.
    for i in range(1, steps):
        x, y = U[2, i-1], U[3, i-1]
        base = ((U[0, i-1]**2.0) + (U[1, i-1]**2.0)) ** 1.5
        vx = -U[0, i-1] / base
        vy = -U[1, i-1] / base

        F = array([x, y, vx, vy])

        def cn(x):
            base = ((x[0] ** 2.0) + (x[1] ** 2.0)) ** 1.5
            return [x[0] - U[0, i-1] - (x[2] + F[0]) * dt / 2,
                    x[1] - U[1, i-1] - (x[3] + F[1]) * dt / 2,
                    x[2] - U[2, i-1] - (-x[0] / base + F[2]) * dt / 2.0,
                    x[3] - U[3, i-1] - (-x[0] / base + F[3]) * dt / 2.0]
        U[:,i] = fsolve(cn, U[:,i-1])

    # Display the points
    fig, ax = plt.subplots()
    ax.plot(U[0,:], U[1,:])

    ax.set(title='Crank-Nicholson orbit')

    plt.show()

def force(nu, x, y):
    distance = math.sqrt((x ** 2) + (y ** 2)) ** 3.0
    factor = nu / distance
    return -factor * x, -factor * y


if __name__ == "__main__":
    compute([1.0, 0.0, 0.0, 1.0], 0.0001, 100000)