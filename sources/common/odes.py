# Common ODEs and mathematic models.



from matplotlib import pyplot as plt

from multiprocessing import Pool, cpu_count as ncpus

from numpy import array, average, empty, float as npfloat, linspace, log10, size, std as deviation, var as variance, zeros, round_
from numpy.linalg import norm
from numpy.typing import ArrayLike

from sklearn.linear_model import LinearRegression

from typing import Callable, Tuple



def Extract(X: Tuple[int, ArrayLike]) -> ArrayLike:
    return X[1]



class IndexFilter:
    def __init__(self, i):
        self.index = 2 ** i

    def __call__(self, x: Tuple[int, ArrayLike]) -> bool:
        return (x[0] % self.index) == 0



def ParCompute(U0: ArrayLike, t: ArrayLike, F: Callable, scheme: Callable, i: int) -> ArrayLike:
    return array( list( map( Extract, filter( IndexFilter(i), enumerate( Cauchy(U0, t, F, scheme) ) ) ) ) )



def Convergencia(U0: ArrayLike, t: ArrayLike, F: Callable, scheme: Callable, samples=5) -> Tuple[ArrayLike, float, float, float]:
    # Calculate final time.
    tf = (t[1] - t[0]) * 100

    # Build the temporal linear spaces.
    time = [linspace(0, tf, (100 * (2 ** i)) + 1) for i in range(samples+1)]

    # Build the multiprocessing pool.
    pool = Pool(processes=ncpus())
    threads = [pool.apply_async(ParCompute, (U0, time[i], F, scheme, i)) for i in range(samples+1)]

    # Collect the results.
    U = [p.get() for p in threads]

    # Build the log E and log N array.
    logE = array( [log10( norm( U[i+1][-1] - U[i][-1] ) ) for i in range(samples)] )
    logN = array( [log10( 100 * (2 ** i) )                for i in range(samples)] )

    # Build the rate of convergence array.
    for j in range(samples):
        if abs(logE[j]) > 12:
            break
    
    j = min(j, samples)

    #print(f"Rate of Convergence {q}")
    reg = LinearRegression().fit(logN[0:j+1].reshape((-1,1)), logE[0:j+1])
    q = round_(abs(reg.coef_), 1)

    logE[:] = logE[:] - log10(1.0 - (1.0 / (2.0 ** q)))

    return q, logE, logN



def ErrorRichardson(U0: ArrayLike, t: ArrayLike, F: Callable, scheme: Callable, order) -> Tuple[ArrayLike, float, float, float]:
    # Extract base values.
    N = size(t)
    M = size(U0)

    # Build the temporal linear spaces.
    t1 = t
    t2 = linspace( 0, t[-1], 2 * N)
    
    # Calculate the results vectors.
    U1 = Cauchy(U0, t1, F, scheme)
    UF = Cauchy(U0, t2, F, scheme)

    # Filter the unwanted U2 values.
    U2 = array( list( map( lambda X: X[1], filter( lambda X: X[0] % 2 == 0, enumerate(UF) ) ) ) )

    # Richardson constant.
    K = 1.0 - ( 1.0 / (2.0 ** order) )

    # Calculate the raw vectorized delta.
    D = array( list( map(lambda U: (U[0] - U[1]), zip( U2, U1 ) ) ) )

    # Calculate the vectorized error.
    A = array( list( map( lambda X: X / K, D ) ) )

    # Calculate the scalar normalized error.
    E = array( list( map( lambda X: norm(X), A ) ) )

    # Calculate the vectorized relative error.
    dp = map( lambda X: norm(X[:2]), U2 )
    dv = map( lambda X: norm(X[2:]), U2 )

    ep = map( lambda X: norm(X[:2]), A )
    ev = map( lambda X: norm(X[2:]), A )

    V = empty([N, 2], dtype=npfloat)

    V[:,0] = array( list( map( lambda X: X[0] / X[1], zip(ep, dp) ) ) )
    V[:,1] = array( list( map( lambda X: X[0] / X[1], zip(ev, dv) ) ) )

    # Calculate the scalar normalized relative error.
    R = array( list( map( lambda X: norm(X), V ) ) )

    return A, E, V, R



def Cauchy(U0: ArrayLike, t: ArrayLike, F: Callable, scheme: Callable) -> ArrayLike:
    # Lenght of the results.
    N = len(t) - 1

    # Build the result vector and initialize it.
    U = zeros([N+1, size(U0)])
    U[0, :] = U0

    # Calculate the result.
    for i in range(N):
        dt = t[i+1] - t[i]
        U[i+1, :] = scheme( U[i, :], dt, t[i], F )

    return U
