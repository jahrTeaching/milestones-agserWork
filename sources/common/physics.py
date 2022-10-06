# Physics equations used in the milestones.



from numpy import array
from numpy.typing import ArrayLike



# Equation step for a Kepler orbit.
def Kepler(U: ArrayLike, t: float):
    x , y  = U[0], U[1]
    dx, dy = U[2], U[3]

    d = ((x ** 2.0) + (y ** 2.0)) ** 1.5

    return array( [dx, dy, -x/d, -y/d] )
