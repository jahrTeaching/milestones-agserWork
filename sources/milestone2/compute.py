# Generic compute method for kepler orbits.



from numpy import array, zeros, dot, size
from numpy.linalg import norm, inv
from scipy.optimize import fsolve



# Euler scheme.
def eu(U, dt, F, t):
    return U + dt * F(U, t)

# Inverse Euler scheme.
def ie(U, dt, F, t):
    fn = lambda x : x - U - F(x, t) * dt

    return fsolve(fn, U)

# Runge-Kutta 4 scheme.
def rk(U, dt, F, t):
    # Get the constants.
    k1 = F(U, t)
    k2 = F(U + dt * k1 / 2.0, t + dt / 2.0)
    k3 = F(U + dt * k2 / 2.0, t + dt / 2.0)
    k4 = F(U + dt * k3, t + dt)

    return U + dt * (k1 + (2.0 * k2) + (2.0 * k3) + k4) / 6.0

# Crank-Nicolson scheme.
def cn(U, dt, F, t):
    fn = lambda x : x - U - (F(x, t) + F(U, t)) * dt / 2.0

    return fsolve(fn, U)

# Jacobiano de matriz.
def jacobiano(F, x):
    N = size(x)
    J = zeros([ N, N ])

    for j in range( N ):
        dx = zeros( N )
        dx[j] = 1e-3

        J[:,j] = ( F(x + dx) - F(x - dx) ) / norm( 2 * 1e-3)

    return J

# Newton method.
def newton(F, x, tol=1e-5, steps=1000):
    N = size(x)
    U = zeros(N)
    U1 = x

    eps = 1
    it = 0

    U = x
    
    while (eps > tol) and (it < steps):
        U = U1 - dot( inv( jacobiano(F, U1) ), F(U1) )
        eps = norm(U - U1)
        U1 = U
        it += 1

        #D = dot( inv( jacobiano(F, U) ), F(U) )
        #U = U - D
        #eps = norm(D)

        #if eps < tol:
        #    return U

    #print(f"Failed to reach tolerance of {tol} (real = {eps}) with {steps} steps. Value: {U}")
    return x

# General Cauchy problem method.
def cauchy(F, t, U0, scheme):
    # Initialize variables.
    N = len(t) - 1
    N0 = len(U0)

    U = array(zeros([N+1, N0]))
    U[0,:] = U0

    # Start looping.
    for i in range(N):
        dt = t[i+1] - t[i]
        U[i+1,:] = scheme(U[i,:], dt, F, t[i])

    return U

# Kepler function.
def kepler(U, t):
    r = U[:-2]
    d = U[2:]
    n = ((r[0]**2.0) + (r[1]**2.0))**0.5

    return array([ d[0], d[1], -r[0]/(n**3.0), -r[1]/(n**3.0) ])

# Specific energy function.
def energy(U, N):
    # Initialize the variables.
    e = array(zeros(N+1))
    mu = 3.986e14

    for i in range(N):
        Em = ((U[i,2]**2.0) + (U[i,3]**2.0)) / 2.0
        Ep = mu / (((U[i,0]**2.0) + (U[i,1]**2.0))**0.5)

        e[i] = Em - Ep

    return e