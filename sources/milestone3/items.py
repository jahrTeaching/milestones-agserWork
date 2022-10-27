# Submenu para el Milestone 3.



from common.config import Config
from common.menu import Menu
from common.odes import Convergencia, ErrorRichardson
from common.physics import Kepler
from common.schemes import Euler, EulerInverso, CrankNicolson, RungeKutta, LeapFrog

from matplotlib import pyplot as plt

from numpy import array, linspace
from numpy.linalg import norm

from typing import Callable



def all(cfg: Config):
    # Build the temporal linear space.
    t = linspace(cfg.getitem("start").value(), cfg.getitem("end").value(), cfg.getitem("steps").value())

    # Build the initial conditions.
    U0 = array([cfg.getitem("X0").value(), cfg.getitem("Y0").value(), cfg.getitem("VX0").value(), cfg.getitem("VY0").value()])

    # Build the order.
    order = cfg.getitem("order").value()

    # Get the results.
    results = [(s.__name__, Convergencia(U0, t, Kepler, s, order)) for s in [Euler, EulerInverso, CrankNicolson, RungeKutta]]

    #Get minimum value for plotting.
    bottom = min( [ min( e ) for (s, (q, e, n)) in results] ) - 1.0

    # Plot all the results.
    fig, ((eu, ei), (cn, rk)) = plt.subplots(2, 2)

    for ((name, (q, logE, logN)), ax) in zip( results, [eu, ei, cn, rk] ):

        # Display information.
        ax.set_title(f"Convergence rate of {name} (Q={q}")
        ax.set_xlabel("log(N)")
        ax.set_ylabel("log(E)")
        ax.set_ylim(bottom, 0.0)

        ax.plot( logN, logE )

    plt.show()

def comp(cfg: Config, scheme: Callable, method: Callable):
    # Build the temporal linear space.
    t = linspace(cfg.getitem("start").value(), cfg.getitem("end").value(), cfg.getitem("steps").value())

    # Build the initial conditions.
    U0 = array([cfg.getitem("X0").value(), cfg.getitem("Y0").value(), cfg.getitem("VX0").value(), cfg.getitem("VY0").value()])

    # Build the order.
    order = cfg.getitem("order").value()

    # Call the method.
    r = method(U0, t, Kepler, scheme, order)

    print(r)


def error(cfg: Config, scheme: Callable, method: Callable):
    # Build the temporal linear space.
    t = linspace(cfg.getitem("start").value(), cfg.getitem("end").value(), cfg.getitem("steps").value())

    # Build the initial conditions.
    U0 = array([cfg.getitem("X0").value(), cfg.getitem("Y0").value(), cfg.getitem("VX0").value(), cfg.getitem("VY0").value()])

    # Build the order.
    order, _, _ = Convergencia(U0, t, Kepler, scheme, cfg.getitem("order").value())

    # Call the method.
    A, E, V, R = method(U0, t, Kepler, scheme, order)

    # Plot the error.
    fig, ((aax, eax), (vax, rax)) = plt.subplots(2, 2)

    # Format the title
    fig.suptitle("Error estimation")

    # Format the vectorized relative error graph.
    aax.set_title("Absolute error per dimension")
    aax.set_xlabel("Time [s]")
    aax.set_ylabel("Absolute error")
    aax.plot(t, A[:,0], 'r', label="X position")
    aax.plot(t, A[:,1], 'g', label="Y position")
    aax.plot(t, A[:,2], 'b', label="X velocity")
    aax.plot(t, A[:,3], 'm', label="Y velocity")
    aax.legend()

    # Format the absolute error graph.
    eax.set_title("Absolute error")
    eax.set_xlabel("Time [s]")
    eax.set_ylabel("Absolute normalized error")
    eax.plot(t, E, 'r')

    # Format the vectorized relative error graph.
    vax.set_title("Relative error per dimension")
    vax.set_xlabel("Time [s]")
    vax.set_ylabel("Relative error [%]")
    vax.plot(t, V[:,0] * 100.0, 'r', label="Position")
    vax.plot(t, V[:,1] * 100.0, 'b', label="Velocity")
    vax.legend()

    # Format the relative error graph.
    rax.set_title("Relative error")
    rax.set_xlabel("Time [s]")
    rax.set_ylabel("Relative normalized error [%]")
    rax.plot(t, R * 100.0, 'r')

    plt.show()



def convergencia(cfg: Config):
    # Build the menu.
    menu = Menu()

    menu.setconfig(cfg)

    menu.additem("euler", 1, "Convergence Rate of Euler",          lambda cfg: comp(cfg, Euler,         Convergencia))
    menu.additem("euinv", 2, "Convergence Rate of Inverse Euler",  lambda cfg: comp(cfg, EulerInverso,  Convergencia))
    menu.additem("crank", 3, "Convergence Rate of Crank-Nicolson", lambda cfg: comp(cfg, CrankNicolson, Convergencia))
    menu.additem("runge", 4, "Convergence Rate of Runge-Kutta 4",  lambda cfg: comp(cfg, RungeKutta,    Convergencia))
    menu.additem("leap",  5, "Convergence Rate of Leap-Frog",      lambda cfg: comp(cfg, LeapFrog,      Convergencia))

    menu.additem("all", "A", "Convergence rate for all schemes",   all)

    menu.menu()



def richardson(cfg: Config):
    # Build the menu.
    menu = Menu()

    menu.setconfig(cfg)

    menu.additem("euler", 1, "Richardson Error of Euler",          lambda cfg: error(cfg, Euler,         ErrorRichardson))
    menu.additem("euinv", 2, "Richardson Error of Inverse Euler",  lambda cfg: error(cfg, EulerInverso,  ErrorRichardson))
    menu.additem("crank", 3, "Richardson Error of Crank-Nicolson", lambda cfg: error(cfg, CrankNicolson, ErrorRichardson))
    menu.additem("runge", 4, "Richardson Error of Runge-Kutta 4",  lambda cfg: error(cfg, RungeKutta,    ErrorRichardson))
    menu.additem("leap",  5, "Richardson Error of Leap-Frog",      lambda cfg: error(cfg, LeapFrog,      ErrorRichardson))

    menu.menu()
