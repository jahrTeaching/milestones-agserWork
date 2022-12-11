# Physics equations used in the milestones.



from ctypes import c_double
from common.algebra import Jacobiano, Newton
from common.color import hue2rgb
from common.config import Config
from common.schemes import RungeKutta
from functools import reduce
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PatchCollection
from multiprocessing import Array, Pool, cpu_count as ncpus
from multiprocessing.sharedctypes import Array
from numpy import array, empty, sqrt, size, reshape, zeros
from numpy.linalg import eig, norm
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



def  CR3BP(U, t, mu=3.0039e-7):
    # Get the dimensionality.
    l = int( len(U) / 2 )

    # Get the position and velocity.
    r = U[:l]
    d = U[l:]

    # Calculate the velocities.
    v = [
        sqrt( ((r[0]     + mu) ** 2) + (r[1]**2) ),
        sqrt( ((r[0] - 1 + mu) ** 2) + (r[1]**2) ),
    ]

    # Calculate the forces.
    f = [
        (-(1-mu) * (r[0] + mu) / (v[0]**3)) - (mu * (r[0] - 1 + mu) / (v[1]**3)),
        (-(1-mu) * (r[1]     ) / (v[0]**3)) - (mu * (r[1]         ) / (v[1]**3)),
    ]

    return array( [
        d[0],
        d[1],

        ( 2 * d[1]) + r[0] + f[0],
        (-2 * d[0]) + r[1] + f[1],
    ] )

def LagrangePoints(U, NL, mu=3.0039e-7):
    # Storage for lagrange points.
    LP = zeros([5,2])

    def F(Y):
        X = zeros(4)
        X[:2] = Y
        X[2:] = 0

        return CR3BP(X, 0, mu)[2:4]

    for i in range(NL):
        LP[i,:] = Newton(F, U[i,:2])

    return LP


def LagrangePointStability(U, mu=3.0039e-7):
    def F(Y):
        return CR3BP(Y, 0, mu)

    A = Jacobiano(F, U)

    values, vectors = eig(A)

    return values


# N-Body problem solver.
def NBody(cfg: Config):
    # Extract the base arguments.
    steps = cfg.getitem('steps').value()
    num = cfg.getitem('num').value()
    dt = cfg.getitem('dt').value()
    com = cfg.getitem('com').value()
    scale = cfg.getitem('scale').value()

    # Create the array and populate the initial step.
    bodies = empty((steps, num, 6))
    bodies[0] = array( [[(random() - 0.5) * scale for _ in range(6)] for _ in range(num)] )

    # Iterate over time.
    for step in range(1, steps):
        bodies[step] = RungeKutta(bodies[step-1], dt, 0.0, NBodyForce)

    # Get the X position.
    X = [ [body[0] for body in step] for step in bodies ]
    Y = [ [body[1] for body in step] for step in bodies ]
    Z = [ [body[2] for body in step] for step in bodies ]
    V = [ [norm(body[3:]) for body in step] for step in bodies ]

    # Renormalize for centre of mass.
    if com:
        for step in range(steps):
            centre = [0.0, 0.0, 0.0]

            for body in range(num):
                centre[0] += X[step][body]
                centre[1] += Y[step][body]
                centre[2] += Z[step][body]

            centre[0] = centre[0] / num
            centre[1] = centre[1] / num
            centre[2] = centre[2] / num

            for body in range(num):
                X[step][body] = X[step][body] - centre[0]
                Y[step][body] = Y[step][body] - centre[1]
                Z[step][body] = Z[step][body] - centre[2]



    # Get the trajectories.
    travel = [[] for _ in range(num)]

    for step in bodies:
        for (j, data) in enumerate( step ):
            travel[j].append( [data[0], data[1], data[2]] )

    travel = array( travel )


    # Transform the V array into colors.

    # Maximum velocity, X and Y value.
    Vmax = max( max(V[:]) )
    Xabs = [ [abs(x) for x in step] for step in X ]
    Yabs = [ [abs(y) for y in step] for step in Y ]
    Zabs = [ [abs(z) for z in step] for step in Z ]

    Xmax = max( [max(x) for x in Xabs] )
    Ymax = max( [max(y) for y in Yabs] )
    Zmax = max( [max(z) for z in Zabs] )
    #Ymax = max( max( map(abs, Y[:] ) ) )

    # Color map.
    #C = [ [hue2rgb(Vel / Vmax) for Vel in step] for step in V ]

    # Display animated problem.
    fig = plt.figure()
    ax  = fig.add_subplot(projection='3d')

    # Initialize the lines.
    lines = []

    for body in travel[:]:
        l = ax.plot([], [], [])[0]
        l.set_data(body[:0, 0], body[:0, 1])
        l.set_3d_properties([body[:0, 2]])
        lines.append(l)

    def plot(i):
        #ax.cla()
        for (body, line) in zip( travel, lines ):
            line.set_data(body[:i,0], body[:i,1])
            line.set_3d_properties(body[:i,2])

        ax.set_zlim(-Zmax, Zmax)
        #ax.set_xlim(-Xmax, Xmax)
        #ax.set_ylim(-Ymax, Ymax)
        #ax.set_zlim(-Zmax, Zmax)

    anim = FuncAnimation(fig=fig, func=plot, frames=steps, interval=10, repeat_delay=3000)

    plt.show()



# Calculates the derivatives in a step of the N-Body problem.
def NBodyForce(U: ArrayLike, t: ArrayLike):
    # Get the size of the physical world.
    Nb = int( len(U)    )
    Nc = int( len(U[0]) )
    Nd = int( Nc / 2 )

    # Get position and velocity pointers.
    Us = reshape(U, (Nb, Nc))
    r = reshape(Us[:, :Nd], (Nb, Nd))
    v = reshape(Us[:, Nd:], (Nb, Nd))

    # Get derivative pointers.
    F = zeros(size(U))
    Fs = reshape(F, (Nb, Nc))
    dr = reshape(Fs[:, :Nd], (Nb, Nd))
    dv = reshape(Fs[:, Nd:], (Nb, Nd))

    # Calculate derivatives.
    #dr[:, :] = v[:, :]
    dv[:, :] = 0

    # Start iteration.
    for i in range(Nb):
        #dv[:, :] = 0
        dr[i, :] = v[i, :]

        for j in range(Nb):
            if i == j:
                continue

            D = r[j, :] - r[i, :]
            dv[i, :] = dv[i, :] + D / norm( D ** 3.0 )

    return reshape(F, (Nb, Nc))
