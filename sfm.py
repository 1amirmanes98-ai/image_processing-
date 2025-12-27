import numpy as np
import matplotlib.pyplot as plt

def f(x):
return np.sin(2 * np.pi * x)

x_data = np.linspace(0.0, 1.0, 10)
y_data = f(x_data)


def phi(t, delta):
return np.maximum(0.0, 1.0 - np.abs(t) / delta)

# --------------------------------------------------
# MLS m = 0 (Shepard)
# --------------------------------------------------

def mls0(x_eval, x_data, y_data, delta):
vals = np.zeros_like(x_eval)
for i, x in enumerate(x_eval):
w = phi(x - x_data, delta)
vals[i] = (w @ y_data) / w.sum()
return vals

# --------------------------------------------------
# MLS m = 1 (local linear)
# --------------------------------------------------

def mls1(x_eval, x_data, y_data, delta):
vals = np.zeros_like(x_eval)
for i, x in enumerate(x_eval):
w = phi(x - x_data, delta)

M0 = np.sum(w)
M1 = np.sum(w * x_data)
M2 = np.sum(w * x_data**2)

F0 = np.sum(w * y_data)
F1 = np.sum(w * y_data * x_data)

D = M0 * M2 - M1**2

a0 = (F0 * M2 - F1 * M1) / D
a1 = (F1 * M0 - F0 * M1) / D

vals[i] = a0 + a1 * x

return vals

# plot


delta = 0.25
x_plot = np.linspace(0.0, 1.0, 300)

y0 = mls0(x_plot, x_data, y_data, delta)
y1 = mls1(x_plot, x_data, y_data, delta)

plt.plot(x_plot, f(x_plot), label="f(x)")
plt.plot(x_plot, y0, "--", label="MLS m=0")
plt.plot(x_plot, y1, "-.", label="MLS m=1")
plt.scatter(x_data, y_data, color="black")
plt.legend()
plt.grid(True)
plt.show()