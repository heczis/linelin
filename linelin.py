"""
1D viscoelastic material model with nonlinear elements.
"""
import numpy as np
import scipy.integrate
import scipy.interpolate

class Material:
    """
    Viscoelastic material model of Zener type with the possibility of
    all three elements (two springs, one damper) to be nonlinear.
    Provides method for computing stress when deformation as a
    function of time is given.
    """
    def __init__(self, Ee=lambda x: 1., Ev=lambda x: 1., c=lambda x: .1):
        """
        Ee, Ev, c: functions of a single scalar argument. Return
          moduli corresponding to the springs and damper.
        """
        self.Ee, self.Ev, self.c = Ee, Ev, c
        return None

    def __call__(self, epsilon):
        """
        epsilon : np.array
          epsilon[0] : time
          epsilon[1] : deformation

        Returns stress in a vector of the same length as epsilon[0].
        """
        ## elastic part:
        sigma_e = np.array([self.Ee(e) * e for e in epsilon[1]])
        ## Maxwell branch:
        e1 = np.zeros_like(sigma_e)
        for ii in range(1, len(e1)):
            de1n = 0
            de = epsilon[1,ii] - epsilon[1,ii-1]
            dt = epsilon[0,ii] - epsilon[0,ii-1]
            for n in range(20):
                de1n = (
                    de - dt * self.Ev(e1[ii-1] + de1n)
                    / self.c((de-de1n)/dt) * e1[ii-1]
                ) / (
                    1 + dt * self.Ev(e1[ii-1] + de1n)
                    /self.c((de-de1n)/dt)
                )
            e1[ii] = e1[ii-1] + de1n

        sigma_v = np.array([self.Ev(e1i) * e1i for e1i in e1])

        return sigma_e + sigma_v
