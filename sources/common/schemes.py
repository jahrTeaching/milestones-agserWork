# Collection of all schemes used in the milestones.



from typing import Callable
from scipy.optimize import newton



# Esquema de Euler explicito.
def Euler(U, dt: float, t: float, F: Callable):
    return U + dt * F(U, t)



# Esquema de Euler inverso.
def EulerInverso(U, dt: float, t: float, F: Callable):
    # Internal residue function.
    residuo = lambda X : X - U - F(X, t) * dt

    return newton(residuo, U)



# Esquema de Crank-Nicolson.
def CrankNicolson(U, dt: float, t: float, F: Callable):
    # Internal residue function.
    residuo = lambda X : X - U - (F(X, t) + F(U, t)) * dt / 2.0

    return newton(residuo, U)
