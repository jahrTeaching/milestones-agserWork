# Embedded Runge-Kutta scheme.



from common.butcher import ButcherArray

from numpy import matmul, zeros
from numpy.linalg import norm



default = ButcherArray.DOPRI54()

def EmbeddedRK(U, dt, t, F, method=default, tol=1e-10):
    # Get the first iteration.
    V1 = RK(U, dt, t, F, method, True )
    V2 = RK(U, dt, t, F, method, False)

    # Get the Butcher array parameters.
    a, b, bs, c, q, Ne = method.parameters()

    # Calculate h.
    h = min(dt, StepSize( V1-V2, tol, dt, min(q) ) )

    # Get the number of intermediate steps.
    Ni = int(dt / h) + 1
    Ndt = dt / Ni

    # Reset V1, V2
    V1 = U
    V2 = U

    first = True

    for i in range(Ni):
        time = t + (i * dt / int(Ni))
        V1 = V2
        if first:
            V2 = RK(V1, time, Ndt, F, method, True)
            first = False
        else:
            V2 = RK(V1, time, Ndt, F, method, False)


    return V2



def RK(U, dt, t, F, method: ButcherArray, first: bool):
    """Performs the given Embedded RK method."""
    # Get the butcher array data.
    a, b, bs, c, q, Ne = method.parameters()

    # Initialize k.
    k = zeros([Ne, len(U)])
    k[0,:] = F(U, t + c[0]*dt)

    for i in range(1, Ne):
        Up = U

        for j in range(i):
            Up = Up + dt * a[i, j] * k[j, :]

        k[i,:] = F(Up, t + c[i] * dt)

    if first:
        return U + dt * matmul(b, k)
    else:
        return U + dt * matmul(bs, k)


def StepSize(dU, tol, dt, q):
    """Returns the correct step size for the next iterartion step."""

    # Error normalizado.
    n = norm(dU)

    if n > tol:
        return dt * (tol / n) ** (1 / (q + 1))
    else:
        return dt