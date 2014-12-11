import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

from linelin import Material

t = np.array([-1, 0, 1, 10])
e = np.array([0, 0, .1, .1])
epsilon = scipy.interpolate.interp1d(
    t, e, kind='linear')

materials = [
    Material(),
    Material(Ee=lambda x:.995 + .01*x),
    Material(Ev=lambda x:.9 + .2*x),
    Material(c =lambda x:.99 + .02*x),
]
mats = [
    r'lin. ($E_{\rm e}=1$, $E_{\rm v} = 1$, $c = 0.1$)',
    r'$E_{\rm e} = 0.995 + 0.01\varepsilon$',
    r'$E_{\rm v} = 0.9 + 0.3\varepsilon_1$',
    r'$c = 0.99 + 0.02\dot\varepsilon$',
]

n = 5
T = np.linspace(min(t), max(t), int((max(t)-min(t)) * n + 1))
E = epsilon(T)

k = [1., 2.]

for ii, mat in enumerate(materials):
    S1 = mat(np.array([T, k[0] * E])) / k[0]
    S2 = mat(np.array([T, k[1] * E])) / k[1]
    plt.plot(T, S1-S2, '.--',
             label='{}'.format(mats[ii]))

plt.grid()
plt.xlabel('t $\mathrm{[s]}$')
plt.ylabel(r'$\sigma(\varepsilon(t)) - \sigma(2\varepsilon(t))/2$')
plt.tight_layout()
plt.legend(loc='best')

plt.show()
