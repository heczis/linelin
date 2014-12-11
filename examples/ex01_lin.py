import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

from linelin import Material

t = np.array([-1, 0, 1, 2, 3]) * 5e0
e = np.array([0, 0, .1, 0, 0])
epsilon = scipy.interpolate.interp1d(
    t, e, kind='linear')

mat = Material()

for n in [3, 10, 20]:
    T = np.linspace(min(t), max(t), int((max(t)-min(t)) * n + 1))
    E = epsilon(T)
    S =  mat(np.array([T, E]))

    plt.figure(0)
    plt.plot(T, E)

    plt.figure(1)
    plt.plot(T, S)

    plt.figure(2)
    plt.plot(E, S)

plt.figure(1)
plt.grid()
plt.show()
