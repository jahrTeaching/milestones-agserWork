# Module containing stability analysis tools for the different temporal schemes.



from common import schemes
from numpy import absolute, array, size, sqrt, zeros
from numpy.typing import ArrayLike
from typing import Callable



def RegionEstabilidad(x: ArrayLike, y: ArrayLike, scheme: Callable) -> ArrayLike:
    # Get the size parameters.
    N = size(x)

    # Generate the complex plane.
    Z = zeros([N, N], dtype=complex)

    # Build into a complex region.
    for i in range(N):
        for j in range(N):
            Z[N-1-j, i] = complex(x[i], y[j])

    return absolute( array( StabilityPolinomial(scheme, Z) ) )

def StabilityPolinomial(scheme: Callable, Z: ArrayLike) -> ArrayLike:
    if scheme == schemes.Euler:
        r = 1.0 + Z
    elif scheme == schemes.EulerInverso:
        r = 1.0 / (1.0 - Z)
    elif scheme == schemes.CrankNicolson:
        r = (1 + (Z / 2.0)) / (1.0 - (Z / 2.0))
    elif scheme == schemes.RungeKutta:
        r = 1 + Z + ((Z ** 2.0) / 2.0) + ((Z ** 3.0) / 6) + ((Z ** 4.0) / 24)
    elif scheme == schemes.LeapFrog:
        r = sqrt(1)

    return r

