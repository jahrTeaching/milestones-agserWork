# Physics equations used in the milestones.



from ctypes import c_double
from common.config import Config
from common.schemes import RungeKutta
from functools import reduce
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from multiprocessing import Array, Pool, cpu_count as ncpus
from multiprocessing.sharedctypes import Array
from numpy import array, empty, frombuffer, size
from numpy.linalg import norm
from numpy.typing import ArrayLike
from random import random



# Equation step for a Kepler orbit.
def Kepler(U: ArrayLike, t: float):
    x , y  = U[0], U[1]
    dx, dy = U[2], U[3]

    d = ((x ** 2.0) + (y ** 2.0)) ** 1.5

    return array( [dx, dy, -x/d, -y/d] )


# Equation step for a Kepler orbit.
def KeplerForce(U: ArrayLike, t: float):
    x , y  = U[0], U[1]
    dx, dy = U[2], U[3]

    d = ((x ** 2.0) + (y ** 2.0)) ** 1.5

    return array( [dx, dy, -x/d, -y/d] )



# N-Body problem solver.
def NBody(cfg: Config):
    # Extract the base arguments.
    num = cfg.getitem('num').value()
    steps = cfg.getitem('steps').value()
    dt = cfg.getitem('dt').value()

    # Calculate the number of processes needed.
    nproc = int(num / ncpus()) + 1

    print(f"Number of cores available: {ncpus()}")
    print(f"Number of items per core: {nproc}")

    # Create the shared array.
    buffer = Array(c_double, 4 * num * steps)
    npbuffer = frombuffer( buffer.get_obj() )
    bodies = npbuffer.reshape((steps, num, 4))

    # Populate the initial step.
    bodies[0] = array( [[random() for _ in range(4)] for _ in range(num)] )

    # Calculate the N-Body problem - Not parallelized.
    #NBodyThread(0, num, num, dt, bodies)

    # Test N-Body with only two bodies.
    bodies = array( [ [ [0.0 for _ in range(4)] for _ in range(2) ] for _ in range(20) ] )
    bodies[0] = array( [[1.0, 0.0, 0.0, 0.0], [-1.0, 0.0, 0.0, 0.0]] )
    NBodyThread(0, 2, 2, dt, bodies)

    # Get the X position.
    X = [ [body[0] for body in step] for step in bodies ]
    Y = [ [body[1] for body in step] for step in bodies ]
    V = [ [norm(body[2:]) for body in step] for step in bodies ]

    # Transform the V array into colors.

    # HUE to RGB transformation function.
    r = lambda v: (5 + (v * 6)) % 6
    g = lambda v: (3 + (v * 6)) % 6
    b = lambda v: (1 + (v * 6)) % 6

    c = lambda k: 1.0 - max( min( [k, 4-k, 1] ), 0 )

    rgb = lambda v: (int(c(r(v))), int(c(g(v))), int(c(b(v))))

    # Maximum velocity value.
    Vmax = max( max(V[:]) )

    # Color map.
    C = [ [rgb(Vel / Vmax) for Vel in step] for step in V ]

    # Display animated problem.
    fig, ax = plt.subplots(figsize = (8, 8))

    def update(frame):
        ax.cla()
        ax.scatter(X[frame], Y[frame], c=C[frame])

    anim = FuncAnimation(fig, update, frames=steps, interval=10, repeat_delay=3000)

    plt.show()


def NBodyThread(s: int, e: int, num: int, dt: float, bodies):
    # Get number of steps.
    steps = len(bodies)

    # Extract function.
    mass = lambda U: (U[0], U[1])

    # Create a sum lambda.
    sum = lambda x, y: (x[0] + y[0], x[1] + y[1])

    # Create a fake U for modifications.
    fake = array( [0.0 for _ in range(4)] )

    for step in range(1, steps):
        # Calculate the whole center of mass.
        red = reduce( sum, map( mass, bodies[step-1] ) )
        (cmx, cmy) = red

        for i in range(s, e):
            # Load the new fake vector.
            fake = bodies[step-1, i]

            # Calculate new center of mass.
            mx, my = (cmx - fake[0]), (cmy - fake[1])

            # Create the new fake vector.
            #fake[0] = fake[0] - mx
            #fake[1] = fake[1] - my

            bodies[step,i,:] = RungeKutta( fake, dt, 0.0, KeplerForce )
