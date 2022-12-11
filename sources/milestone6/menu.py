# Menu selector of milestone 6



from common.menu import Menu
from common.odes import Cauchy
from common.physics import LagrangePoints, LagrangePointStability, CR3BP
from common.erk import EmbeddedRK

from matplotlib import pyplot as plt

from numpy import around, array, zeros, linspace

from random import random


def menu():
    # Create the menu.
    menu = Menu()

    menu.additem("vmun" , 1, "Earth-Moon Lagrange points", lambda: LPValues(1.2151e-2) )
    menu.additem("vsun" , 2, "Earth-Sun Lagrange points" , lambda: LPValues(3.0039e-7) )

    menu.additem("omun" , 3, "Earth-Moon Lagrange orbits", lambda: LPOrbitsMenu(1.2151e-2, 1e-2) )
    menu.additem("osun" , 4, "Earth-Sun Lagrange orbits" , lambda: LPOrbitsMenu(3.0039e-6, 1e-2) )

    menu.menu()



def LPValues(mu: float):
    # Approximate Lagrange points.
    U0 = zeros([5, 4])

    U0[0,:] = array([ 0.8,  0.6, 0.0, 0.0])
    U0[1,:] = array([ 0.8, -0.6, 0.0, 0.0])
    U0[2,:] = array([-0.1,  0.0, 0.0, 0.0])
    U0[3,:] = array([ 0.1,  0.0, 0.0, 0.0])
    U0[4,:] = array([1.01,  0.0, 0.0, 0.0])

    # Calculate the Lagrange points.
    xp = LagrangePoints(U0, 5, mu)

    print(xp)

    return xp

def LPOrbitsMenu(mu: float, eps=1e-3):
    menu = Menu()

    menu.additem("l1" , 1, "Lagrange Point 1", lambda: LPOrbits(mu, 1, eps) )
    menu.additem("l2" , 2, "Lagrange Point 2", lambda: LPOrbits(mu, 2, eps) )
    menu.additem("l3" , 3, "Lagrange Point 3", lambda: LPOrbits(mu, 3, eps) )
    menu.additem("l4" , 4, "Lagrange Point 4", lambda: LPOrbits(mu, 4, eps) )
    menu.additem("l5" , 5, "Lagrange Point 5", lambda: LPOrbits(mu, 5, eps) )

    menu.menu()


def LPOrbits(mu: float, lp=1, eps=1e-3):
    # Get the values of the points.
    xp = LPValues(mu)

    # Create the orbits.
    U0LP = zeros(4)

    U0LP[:2] = xp[lp-1,:] + (random() * eps)
    U0LP[2:] = (random() * eps)

    U0SLP = zeros(4)

    U0SLP[:2] = xp[lp-1,:]
    U0SLP[2:] = 0

    # Stability of Lagrange points
    def F(U, t):
        return CR3BP(U, t, mu)

    ULP = Cauchy(U0LP, linspace(0, 100, 10000), F, EmbeddedRK)

    eigenvalues = LagrangePointStability(U0SLP, mu)

    print(around(eigenvalues.real, 8))

    # Paint the orbits
    fig, (ax1, ax2) = plt.subplots(1, 2)

    # Lagrange Points
    ax1.plot(ULP[:,0], ULP[:,1], '-', color='r')
    ax1.plot(-mu, 0, 'o', color='g')
    ax1.plot(1-mu, 0, 'o', color='b')

    for i in range(5):
        ax1.plot(xp[i,0], xp[i,1], 'o', color='k')

    ax1.set_xlim(-3,3)
    ax1.set_ylim(-3,3)

    ax1.set_title("Orbital system view")

    # Orbits
    ax2.plot(ULP[:,0], ULP[:,1], '-',color="r")
    ax2.plot(xp[lp-1,0], xp[lp-1,1], 'o', color='k')

    ax2.set_title("Lagrage point view")
    ax2.set_xlim(xp[lp-1,0] - 0.5, xp[lp-1,0] + 0.5)
    ax2.set_ylim(xp[lp-1,1] - 0.5, xp[lp-1,1] + 0.5)

    for ax in fig.get_axes():
        ax.set(xlabel='x', ylabel='y')
        ax.grid()

    plt.show()

