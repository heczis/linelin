import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

from linelin import Material

t = np.array([-1, 0, 0, 2])
e = np.array([0, 0, .1, .1])
epsilon = scipy.interpolate.interp1d(
    t, e, kind='linear')

# linear material:
mat = Material()
# different nonlinear materials:
nl_materials = [
    Material(Ee=lambda x:.995 + .025*x),
    Material(Ev=lambda x:.9 + .5*x),
    Material(c =lambda x:.09 + .05*x),
]
mats = [
    r'$E_{\rm e} = 0.995 + 0.01\varepsilon$',
    r'$E_{\rm v} = 0.9 + 0.2\varepsilon_1$',
    r'$c = 0.995 + 0.01\dot\varepsilon$',
]

n = 30
T = np.linspace(min(t), max(t), int((max(t)-min(t)) * n + 1))
E = epsilon(T)

stoptol = 1e-6

S = mat(np.array([T, E]), stoptol=stoptol)

for ii, mat in enumerate(nl_materials):
    S1 = mat(np.array([T, E]), stoptol=stoptol)
    plt.figure(0)
    plt.plot(T, S1, '.--', label=mats[ii])
    plt.figure(1)
    plt.plot(T, S1-S, '.--', label=mats[ii])

plt.figure(0)
plt.plot(T, S, '.--', label='linear')

plt.figure(0)
plt.ylabel(r'$\sigma(\varepsilon(t))$')
plt.figure(1)
plt.ylabel(r'$\sigma(\varepsilon(t)) - \sigma_{\rm lin}(\varepsilon(t))$')

for ii in [0, 1]:
    plt.figure(ii)
    plt.grid()
    plt.xlabel('$t$ $\mathrm{[s]}$')
    plt.legend(loc='best')
    plt.tight_layout()

plt.show()
