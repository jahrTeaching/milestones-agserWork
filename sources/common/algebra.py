# Algebra methods used in the milestones.



from numpy import dot, size, zeros
from numpy.linalg import norm



def FactorizeLU(A):
    # Extract dimensions and build base matrix.
    N = size(A, 1)
    U = zeros([N, N])
    L = zeros([N, N])

    # Initialize U.
    U[0,:] = A[0,:]

    # Initialize L.
    for i in range(N):
        L[i,i] = 1
    L[1:N,0] = A[1:N,0] / U[0,0]

    for i in range(1, N):

        for j in range(i, N):
            U[i,j] = A[i,j] - dot( L[i,:i], U[:i,j] )

        for k in range(i+1, N):
            L[k, i] = ( A[k, i] - dot( U[:i,i], L[k,:i] ) ) / U[i,i]

    return [L@U, L, U]

def SolveLU(M, b):
    # Extract dimensions.
    N = size(b)

    # Build base arrays.
    X, Y = zeros(N), zeros(N)

    # Factorize the matrix.
    A, L, U = FactorizeLU(M)

    # Initialize array and compute Y.
    Y[0] = b[0]

    for i in range(N):
        Y[i] = b[i] - dot(A[i,:i], Y[:i])

    X[N-1] = Y[N-1] / A[N-1,N-1]

    for i in range(N-2, -1, -1):
        X[i] = ( Y[i] - dot( A[i, i+1:N+1], X[i+1:N+1] ) ) / A[i,i]

    return X

def Inverse(A):
    # Extract dimensions and initialize matrix.
    N = size(A, 1)
    B = zeros([N, N])

    for i in range(N):
        one = zeros(N)
        one[i] = 1.0

        B[:,i] = SolveLU(A, one)

    return B

def Jacobiano(F, U):
    # Get the size of the array.
    N = size(U)

    if N == 1:
        x = 1e-3
        return (F(U + x) - F(U - x)) / (2 * x)

    N = size(U)
    J = zeros([N, N])

    for i in range(N):
        x = zeros(N)
        x[i] = 1e-3
        J[:,i] = (F(U + x) - F(U - x)) / 2e-3

    return J

def Newton(f, U0, tol=1e-8, steps=1000):
    # Extract dimensions and initialize.
    N = size(U0)
    error = 1

    if N == 1:
        def prime(F, x):
            return (F(x + 10e-6) - F(x - 10e-6)) / 20e-6

        U = 0.0
        U1 = U0

        for step in range(steps):
            if error <= tol:
                return U

            U = U1 - f(U1) / prime(f, U1)

            error = abs(U - U1)


            U1 = U

        print(f"[WARNING] Newton method reached max steps ({steps})")

        return U

    U = zeros(N)
    U1 = U0


    for step in range(steps):
        if error <= tol:
            break

        U = U1 - dot( Inverse( Jacobiano(f, U1) ), f(U1) )

        error = norm(U - U1)

        U1 = U

    if step >= (steps - 1):
        print(f"[WARNING] Newton method reached max steps ({steps})")

    return U
