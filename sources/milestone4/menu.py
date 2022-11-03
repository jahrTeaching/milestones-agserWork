# Menu selector of milestone 4



from common.config import Config
from common.menu import Menu

from common import schemes
from common.config import Config
from common.stability import RegionEstabilidad
from matplotlib import pyplot as plt
from numpy import array, linspace
from typing import Callable



def menu():
    menu = Menu()

    menu.additem("eu", 1, "Stability Region of Euler",          lambda : region(schemes.Euler)        )
    menu.additem("ie", 2, "Stability Region of Inverse Euler",  lambda : region(schemes.EulerInverso) )
    menu.additem("ie", 3, "Stability Region of Crank Nicolson", lambda : region(schemes.CrankNicolson))
    menu.additem("ie", 4, "Stability Region of Runge-Kutta 4",  lambda : region(schemes.RungeKutta)   )
    menu.additem("ie", 5, "Stability Region of Leap-Frog",      lambda : region(schemes.LeapFrog)     )

    menu.menu()

def region(scheme: Callable):
    # Default configuration.
    N = 500
    X = linspace(-6, 6, N)
    Y = linspace(-6, 6, N)

    # Calculate the stability region.
    region = RegionEstabilidad(X, Y, scheme)

    # Plot the stability region.
    CSF = plt.contourf(X, Y, region, levels=[0,1], colors=['#E0E0E0'])
    #CS = plt.contour(X, Y, region, levels = [0.25, 0.5, 0.75, 1, 1.25, 1.5])
    CS = plt.contour(X, Y, region, levels = [0.1 * (i+1) for i in range(15)])

    plt.title(f'Region de Estabilidad Absoluta de {scheme.__name__}')
    plt.xlabel('Re(|r|)')
    plt.ylabel('Im(|r|)')

    plt.xlim([-4, 4])
    plt.ylim([-4, 4])

    plt.legend(loc = "lower left")

    plt.grid()
    plt.show()
