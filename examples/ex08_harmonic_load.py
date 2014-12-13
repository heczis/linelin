import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

from linelin import Material

t = np.linspace(0, 20*np.pi, 201)
e = np.sin(t)
epsilon = scipy.interpolate.interp1d(
    t, e, kind='linear')

# linear material:
mat = Material()
# different nonlinear materials:
Ee_fun = lambda x:.95 + .05*x
Ev_fun = lambda x:.9 + .5*x
c_fun = lambda x:.09 + .05*x
nl_materials = [
    Material(Ee=Ee_fun),
    Material(Ev=Ev_fun),
    Material(c =c_fun),
]
mats = [
    r'$E_{{\rm e}} = {:.3f} + {:.3f}\varepsilon$'.format(
        Ee_fun(0), Ee_fun(1)-Ee_fun(0)),
    r'$E_{{\rm v}} = {:.3f} + {:.3f}\varepsilon_1$'.format(
        Ev_fun(0), Ev_fun(1)-Ev_fun(0)),
    r'$c = {:.3f} + {:.3f}\dot\varepsilon$'.format(
        c_fun(0), c_fun(1)-c_fun(0)),
]

n = 10
T = np.linspace(min(t), max(t), int((max(t)-min(t)) * n + 1))
E = epsilon(T)

stoptol = 1e-6

S = mat(np.array([T, E]), stoptol=stoptol)

for ii, mat in enumerate(nl_materials):
    S1 = mat(np.array([T, E]), stoptol=stoptol)
    plt.figure(0)
    plt.plot(T, S1, label=mats[ii])
    plt.figure(1)
    plt.plot(T, S1-S, label=mats[ii])
    plt.figure(2)
    plt.plot(E, S1, label=mats[ii])

plt.figure(0)
plt.plot(T, S, label='lin.')
plt.figure(2)
plt.plot(E, S, label='lin.')

for ii in [0, 1, 2]:
    plt.figure(ii)
    plt.grid()
    plt.xlabel('$t$ $\mathrm{[s]}$')
    plt.ylabel(r'$\sigma(\varepsilon(t))$')
    plt.legend(loc='best')
    plt.tight_layout()

plt.figure(1)
plt.ylabel(r'$\sigma(\varepsilon(t)) - \sigma_{\rm lin}(\varepsilon(t))$')
plt.figure(2)
plt.xlabel(r'$\varepsilon$')

plt.show()
