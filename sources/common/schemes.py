# Collection of all schemes used in the milestones.



from .algebra import Newton

from numpy import size
from numpy.typing import ArrayLike
from typing import Callable



# Esquema de Euler explicito.
def Euler(U: ArrayLike, dt: float, t: float, F: Callable) -> ArrayLike:
    return U + dt * F(U, t)



# Esquema de Euler inverso.
def EulerInverso(U: ArrayLike, dt: float, t: float, F: Callable) -> ArrayLike:
    # Internal residue function.
    residuo = lambda X : X - U - F(X, t) * dt

    return Newton(residuo, U)



# Esquema de Crank-Nicolson.
def CrankNicolson(U: ArrayLike, dt: float, t: float, F: Callable) -> ArrayLike:
    # Internal residue function.
    residuo = lambda X : X - U - (F(X, t) + F(U, t)) * dt / 2.0

    return Newton(residuo, U)

# Esquema de Runge-Kutta 4.
def RungeKutta(U: ArrayLike, dt: float, t: float, F: Callable):
    # Get the constants.
    k1 = F(U, t)
    k2 = F(U + dt * k1 / 2.0, t + dt / 2.0)
    k3 = F(U + dt * k2 / 2.0, t + dt / 2.0)
    k4 = F(U + dt * k3, t + dt)

    return U + dt * (k1 + (2.0 * k2) + (2.0 * k3) + k4) / 6.0

# Esquema de Leap-Frog
def LeapFrog(U: ArrayLike, dt: float, t: float, F: Callable):
    # Assume first half is X and second half is X'.
    l = size(U)[0] / 2

    # Get base.
    X = U

    # Calculate acceleration at i.
    A = F(X, t)

    # Calculate the new position and halfstep velocity.
    X[l:] += A[l:] * dt / 2.0
    X[:l] += X[l:] * dt

    # Calculate the acceleration at i+1.
    A = F(X, t)

    # Calculate the new velocity.
    X[l:] += A[l:] * dt / 2.0

    return X
