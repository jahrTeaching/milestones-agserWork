# Physics equations used in the milestones.



from ctypes import c_double
from common.color import hue2rgb
from common.config import Config
from common.schemes import RungeKutta
from functools import reduce
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from multiprocessing import Array, Pool, cpu_count as ncpus
from multiprocessing.sharedctypes import Array
from numpy import array, empty, frombuffer, size, reshape
from numpy.linalg import norm
from numpy.typing import ArrayLike
from random import random



# Equation step for a Kepler orbit.
def Kepler(U: ArrayLike, t: float):
    x , y  = U[0], U[1]
    dx, dy = U[2], U[3]

    d = ((x ** 2.0) + (y ** 2.0)) ** 1.5

    return array( [dx, dy, -x/d, -y/d] )



# Harmonic Oscillator equation.
def Oscilador(U: ArrayLike, t: float):
    return array([U[1], -U[0]])



# Equation step for a Kepler orbit.
def KeplerForce(U: ArrayLike, t: float):
    x , y  = U[0], U[1]
    dx, dy = U[2], U[3]

    d = ((x ** 2.0) + (y ** 2.0)) ** 1.5

    return array( [dx, dy, -x/d, -y/d] )



# N-Body problem solver.
def NBody(cfg: Config):
    # Extract the base arguments.
    steps = cfg.getitem('steps').value()
    num = cfg.getitem('num').value()
    dt = cfg.getitem('dt').value()

    # Create the array and populate the initial step.
    bodies = empty((steps, num, 4))
    bodies[0] = array( [[(random() - 0.5) for _ in range(4)] for _ in range(num)] )

    # Iterate over time.
    for step in range(1, steps):
        bodies[step] = RungeKutta(bodies[step-1], dt, 0.0, NBodyForce)

    # Get the X position.
    X = [ [body[0] for body in step] for step in bodies ]
    Y = [ [body[1] for body in step] for step in bodies ]
    V = [ [norm(body[2:]) for body in step] for step in bodies ]

    # Transform the V array into colors.

    # Maximum velocity, X and Y value.
    Vmax = max( max(V[:]) )
    Xabs = [ [abs(x) for x in step] for step in X ]
    Yabs = [ [abs(y) for y in step] for step in Y ]

    Xmax = max( [max(x) for x in Xabs] )
    Ymax = max( [max(y) for y in Yabs] )
    #Ymax = max( max( map(abs, Y[:] ) ) )

    # Color map.
    C = [ [hue2rgb(Vel / Vmax) for Vel in step] for step in V ]

    # Display animated problem.
    fig, ax = plt.subplots(figsize = (8, 8))

    def init():
        ax.cla()
        ax.plot([],[])

    def plot(i):
        ax.cla()
        ax.scatter(X[i], Y[i], c=C[i])
        ax.set_xlim(-Xmax, Xmax)
        ax.set_ylim(-Ymax, Ymax)

    anim = FuncAnimation(fig=fig, func=plot, frames=steps, interval=10, repeat_delay=3000)

    plt.show()


# Calculates the derivatives in a step of the N-Body problem.
def NBodyForce(U: ArrayLike, t: ArrayLike):
    # Get the size of the physical world.
    Nb = int( len(U)    )
    Nc = int( len(U[0]) )

    # Get position and velocity pointers.
    Us = reshape(U, (Nb, Nc))
    r = reshape(Us[:, :2], (Nb, 2))
    v = reshape(Us[:, 2:], (Nb, 2))

    # Get derivative pointers.
    F = empty(size(U))
    Fs = reshape(F, (Nb, Nc))
    dr = reshape(Fs[:, :2], (Nb, 2))
    dv = reshape(Fs[:, 2:], (Nb, 2))

    # Calculate derivatives.
    dr[:, :] = v[:, :]

    # Start iteration.
    for i in range(Nb):
        dv[:, :] = 0

        for j in range(Nb):
            if i == j:
                continue
            
            D = r[j, :] - r[i, :]
            dv[:, :] = D / norm( D ** 3.0 )

    return reshape(F, (Nb, Nc))
