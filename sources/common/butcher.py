# Butcher Array implementation.



from numpy import array, zeros



class ButcherArray:
    def __init__(self, a, b, bs, c, q, Ne):
        self.a = a
        self.b = b
        self.bs = bs
        self.c = c
        self.q = q
        self.Ne = Ne

    def parameters(self):
        """Returns the parameters of this Butcher array."""
        return self.a, self.b, self.bs, self.c, self.q, self.Ne

    def HeunEuler():
        """Returns the HeunEuler Butcher Array for the embedded runge-Kutta"""

        # Q values.
        q = [2, 1]

        # Number of steps.
        Ne = 2

        # Create a, b, bs, c.
        a = zeros([Ne, Ne-1])

        # Initialize b and bs.
        b  = array( [ 1./2., 1./2. ] )
        bs = array( [  1.  ,  0.   ] )

        # Initialize c.
        c = array([0., 1.])

        # Initialize a.
        a[0,:] = [ 0. ]
        a[1,:] = [ 1. ]

        return ButcherArray(a, b, bs, c, q, Ne)

    def RK21():
        """Returns the RK21 Butcher Array for the embedded runge-Kutta"""

        # Q values.
        q = [2, 1]

        # Number of steps.
        Ne = 3

        # Create a, b, bs, c.
        a = zeros([Ne, Ne-1])

        # Initialize b and bs.
        b  = array( [ 1./256., 255./256.,  0.    ] )
        bs = array( [ 1./512., 255./256., 1./512.] )

        # Initialize c.
        c = array([0., 0.5, 1.])

        # Initialize a.
        a[0,:] = [   0.    ,    0.    ]
        a[1,:] = [  1./2.  ,    0.    ]
        a[2,:] = [  1./256., 255./256 ]

        return ButcherArray(a, b, bs, c, q, Ne)


    def BogackiShampine():
        """Returns the BogackiShampine Butcher Array for the embedded runge-Kutta"""

        # Q values.
        q = [3, 2]

        # Number of steps.
        Ne = 4

        # Create a, b, bs, c.
        a = zeros([Ne, Ne-1])

        # Initialize b and bs.
        b  = array( [ 2./9. , 1./3., 4./9.,	 0.  ] )
        bs = array( [ 7./24., 1./4., 1./3.,	1./8 ] )

        # Initialize c.
        c = array([0., 1./2., 3./4., 1.])

        # Initialize a.
        a[0,:] = [  0.  ,  0.  ,  0.   ]
        a[1,:] = [ 1./2.,  0.  ,  0.   ]
        a[2,:] = [  0.  , 3./4.,  0.   ]
        a[3,:] = [ 2./9., 1./3., 4./9. ]

        return ButcherArray(a, b, bs, c, q, Ne)



    def DOPRI54():
        """Returns the DOPRI54 Butcher Array for the embedded runge-Kutta"""

        # Q values.
        q = [5, 4]

        # Number of steps.
        Ne = 7

        # Create a, b, bs, c.
        a = zeros([Ne, Ne-1])

        # Initialize b and bs.
        b  = array( [  35./384.  , 0.,  500./1113. ,  125./192.,  -2187./6784.  ,  11./84.  ,   0.  ] )
        bs = array( [5179./57600., 0., 7571./16695.,  393./640., -92097./339200., 187./2100., 1./40 ]  )

        # Initialize c.
        c = array([0., 1./5., 3./10., 4./5., 8./9., 1., 1.])

        # Initialize a.
        a[0,:] = [      0.     ,       0.     ,       0.     ,      0.    ,      0.      ,   0.   ]
        a[1,:] = [     1./5.   ,       0.     ,       0.     ,      0.    ,      0.      ,   0.   ]
        a[2,: ]= [     3./40.  ,      9./40.  ,       0.     ,      0.    ,      0.      ,   0.   ]
        a[3,:] = [    44./45.  ,    -56./15.  ,     32./9.   ,      0.    ,      0.      ,   0.   ]
        a[4,:] = [ 19372./6561., -25360./2187.,  64448./6561.,  -212./729.,      0.      ,   0.   ]
        a[5,:] = [  9017./3168.,   -355./33.  ,  46732./5247.,    49./176., -5103./18656.,   0.   ]
        a[6,:] = [    35./384. ,       0.     ,    500./1113.,   125./192., -2187./6784. , 11./84 ]

        return ButcherArray(a, b, bs, c, q, Ne)

    def CashKarp():
        """Returns the CashKarp Butcher Array for the embedded runge-Kutta"""

        # Q values.
        q = [5, 4]

        # Number of steps.
        Ne = 6

        # Create a, b, bs, c.
        a = zeros([Ne, Ne-1])

        # Initialize b and bs.
        b  = array( [  37./378.,   0.,   250./621.,     125./594.,            0., 512./1771.] )
        bs = array( [2825./27648., 0., 18575./48384., 13525./55296., 277./14336.,   1./4.   ] )

        # Initialize c.
        c = array([0., 1./5., 3./10., 3./5., 1., 7./8.])

        # Initialize a.
        a[0,:] = [    0.      ,    0.    ,    0.      ,      0.       ,    0.     ]
        a[1,:] = [   1./5.    ,    0.    ,    0.      ,      0.       ,    0.     ]
        a[2,:] = [   3./40.   ,   9./40. ,    0.      ,      0.       ,    0.     ]
        a[3,:] = [   3./10.   ,  -9./10. ,   6./5.    ,      0.       ,    0.     ]
        a[4,:] = [ -11./54.   ,   5./2.  , -70./27.   ,    35./27.    ,    0.     ]
        a[5,:] = [1631./55296., 175./512., 575./13824., 44275./110592., 253./4096.]


        return ButcherArray(a, b, bs, c, q, Ne)
