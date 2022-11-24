# Module containing stability analysis tools for the different temporal schemes.


import math


from numpy import zeros, linspace
from typing import Callable



def RegionEstabilidad(scheme: Callable):
    # Define complex region.
    N = 100
    R = linspace(-5, 5, N)
    I = linspace(-5, 5, N)

    # Create the complex map.
    w = zeros([N, N], dtype=complex)
    Z = zeros([N, N], dtype=complex)

    for i in range(N):
        for j in range(N):
            c = complex(R[i], I[j])
            P = lambda U, t: c * U
            
            Z[j, i] = scheme(1.0, 1.0, 0, P)

    return Z
