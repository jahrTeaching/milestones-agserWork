# Menu selector of milestone 4



from common.config import Config
from common.menu import Menu

from common import schemes
from common.config import Config
from common.odes import Cauchy
from common.physics import Oscilador
from common.stability import RegionEstabilidad
from matplotlib import pyplot as plt
from numpy import array, linspace, cos, sin, absolute
from typing import Callable



def menu():
    menu = Menu()

    menu.additem("oscil",  1, "Calculate oscilator movement", oscilmenu)
    menu.additem("region", 2, "Visualize Stability Region",  regionmenu)

    menu.menu()

def oscilmenu():
    menu = Menu()

    menu.additem("eu", 1, "Euler",          lambda : oscillator(schemes.Euler)        )
    menu.additem("ie", 2, "Inverse Euler",  lambda : oscillator(schemes.EulerInverso) )
    menu.additem("ie", 3, "Crank Nicolson", lambda : oscillator(schemes.CrankNicolson))
    menu.additem("ie", 4, "Runge-Kutta 4",  lambda : oscillator(schemes.RungeKutta)   )
    menu.additem("ie", 5, "Leap-Frog",      lambda : oscillator(schemes.LeapFrog)     )

    menu.menu()

def regionmenu():
    menu = Menu()

    menu.additem("eu", 1, "Stability Region of Euler",          lambda : region(schemes.Euler)        )
    menu.additem("ie", 2, "Stability Region of Inverse Euler",  lambda : region(schemes.EulerInverso) )
    menu.additem("ie", 3, "Stability Region of Crank Nicolson", lambda : region(schemes.CrankNicolson))
    menu.additem("ie", 4, "Stability Region of Runge-Kutta 4",  lambda : region(schemes.RungeKutta)   )
    #menu.additem("ie", 5, "Stability Region of Leap-Frog",      lambda : region(LeapFrogModified)     )

    menu.menu()


def oscillator(scheme: Callable):
    # Default configuration.
    N = 100
    U0 = array([1,0]) 
    t = linspace(0, 10, N)

    U = Cauchy( U0, t, Oscilador, scheme)

    fig, (xax, vax) = plt.subplots(1, 2)

    xax.plot(t, U[:,0],"r", label = "Solución Numérica")
    xax.plot(t, cos(t),"--",color = "r", label = "Solución Analítica")

    vax.plot(t, U[:,1],"g", label = "Velocidad Numérica")
    vax.plot(t, -sin(t),"--",color = "g", label = "Velocidad Analítica")

    plt.title(f"Oscilador Armónico para esquema {scheme.__name__}")

    xax.set_xlabel("t")
    xax.set_ylabel("x(t)")
    xax.legend(loc="lower left")

    vax.set_xlabel("t")
    vax.set_ylabel("v(t)")
    vax.legend(loc="lower left")

    xax.grid()
    plt.show()



def region(scheme: Callable):
    # Default configuration.
    N = 100
    X = linspace(-5, 5, N)
    Y = linspace(-5, 5, N)

    # Calculate the stability region.
    region = absolute( RegionEstabilidad(scheme) )

    # Plot the stability region.
    CSF = plt.contourf(X, Y, region, levels=[0,1], colors=['#E0E0E0'])
    #CS = plt.contour(X, Y, region, levels = [0.25, 0.5, 0.75, 1, 1.25, 1.5])
    CS = plt.contour(X, Y, region, levels = [0.1 * (i+1) for i in range(15)])

    plt.title(f'Region de Estabilidad Absoluta de {scheme.__name__}')
    plt.xlabel('Re(|r|)')
    plt.ylabel('Im(|r|)')

    plt.xlim([-5, 5])
    plt.ylim([-5, 5])

    plt.legend(loc = "lower left")

    plt.grid()
    plt.show()
