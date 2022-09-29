# Functions called by the menu items.



from . import compute
from numpy import array, linspace

import matplotlib.pyplot as plt



# Computes the Euler scheme with the given configuration.
def eu(cfg):
    comp(compute.eu, cfg, "Euler")

def ie(cfg):
    comp(compute.ie, cfg, "Inverse Euler")

def rk(cfg):
    comp(compute.rk, cfg, "Runge-Kutta 4")

def cn(cfg):
    comp(compute.cn, cfg, "Crank-Nicolson")


def orbits(cfg):
    # Build the time space.
    t = linspace(0, cfg.tmax, cfg.steps)

    # Calculate the orbits.
    U = []
    U.append( compute.cauchy( compute.kepler, t, array(cfg.start), compute.eu ) )
    U.append( compute.cauchy( compute.kepler, t, array(cfg.start), compute.ie ) )
    U.append( compute.cauchy( compute.kepler, t, array(cfg.start), compute.rk ) )
    U.append( compute.cauchy( compute.kepler, t, array(cfg.start), compute.cn ) )

    # Display the results.

    # Plot the orbits.
    plt.plot(U[0][:,0], U[0][:,1], "r", label="Euler")
    plt.plot(U[1][:,0], U[1][:,1], "g", label="Inverse Euler")
    plt.plot(U[2][:,0], U[2][:,1], "b", label="Runge-Kutta 4")
    plt.plot(U[3][:,0], U[3][:,1], "m", label="Crank-Nicolson")
    plt.title("Orbits")
    plt.legend(loc="lower right")

    plt.show()

def energies(cfg):
    # Build the time space.
    t = linspace(0, cfg.tmax, cfg.steps)

    # Calculate the orbits.
    U = []
    U.append( compute.cauchy( compute.kepler, t, array(cfg.start), compute.eu ) )
    U.append( compute.cauchy( compute.kepler, t, array(cfg.start), compute.ie ) )
    U.append( compute.cauchy( compute.kepler, t, array(cfg.start), compute.rk ) )
    U.append( compute.cauchy( compute.kepler, t, array(cfg.start), compute.cn ) )

    # Calculate the energies.
    e = [compute.energy(u, cfg.steps) for u in U]

    # Display the results.

    # Plot the energy.
    plt.plot(t, e[0][0:len(t)], "r", label="Euler")
    plt.plot(t, e[2][0:len(t)], "g", label="Runge-Kutta 4")
    plt.plot(t, e[1][0:len(t)], "b", label="Inverse Euler")
    plt.plot(t, e[3][0:len(t)], "m", label="Crank-Nicolson")
    plt.title("Energy")
    plt.xlabel("Time [s]")
    plt.ylabel("Energy [J]")
    plt.legend(loc="lower right")

    plt.show()


# General compute function.
def comp(F, cfg, name):
    # Build the time space.
    t = linspace(0, cfg.tmax, cfg.steps)

    # Calculate the orbit.
    U = compute.cauchy( compute.kepler, t, array(cfg.start), F )

    # Calculate the energy.
    e = compute.energy(U, cfg.steps)

    # Display the results.
    display(U, t, e, name)

# Common method to display the results.
def display(U, t, e, name):
    # Get the musltiple subplots.
    fig, axs = plt.subplots(1, 2)

    # Plot the orbit.
    axs[0].plot(U[:,0], U[:,1])
    axs[0].set_title(f"{name} orbit")

    # Plot the energy.
    axs[1].plot(t, e[0:len(t)])
    axs[1].set_title(f"{name} energy")
    axs[1].set(xlabel="Time [s]", ylabel="Energy [J]")

    plt.show()
