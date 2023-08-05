'''
========================
3D surface (solid color)
========================

Demonstrates a very basic plot of a 3D surface using a solid color.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from pyibex import *
from pyibex.image import *
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from pyibex import *
from pyibex.image import *


# import numpy as np
X = np.linspace(-10,10,20)
Y = np.linspace(-10,10,20)
x, y = np.meshgrid(X, Y)
d = np.sqrt(x*x+y*y)
sigma, mu = 2.0, 0.0
g = np.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) )
print("2D Gaussian-like array:")
# print(g)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Plot the surface

# Plot the surface.
surf = ax.plot_surface(x, y, g, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

class mtCtc(Ctc):
    def __init__(self, *args):
        Ctc.__init__(self, 2)
        self.ctc = CtcDataSet(*args)
    def contract(self, X):
        Y = cart_prod(X, IntervalVector(1, [-0.8,1]))
        print(X, Y)
        self.ctc.contract(Y)
        X &= Y.subvector(0,1)

from vibes import vibes
vibes.beginDrawing()
print(g.shape)
ctc = mtCtc(g, X[0], Y[0], X[1]-X[0], Y[1]-Y[0])
X0 = IntervalVector(2, [-8,8])
# X0 = IntervalVector(2, [-8.2,-8.1])
pySIVIA(X0, ctc, 0.5)


# plt.show()

