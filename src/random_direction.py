#!/usr/bin/env python
# coding=utf-8
#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
N = 5000

def get_randU(N=100):
    u01 = np.random.uniform(-1, 1, [N * 2, 2])
    u23 = np.random.uniform(-1, 1, [N * 2, 2])
    bool01 = (u01**2).sum(axis=1) <= 1.
    bool23 = (u23**2).sum(axis=1) <= 1.
    u01 = u01[bool01][:N]
    u23 = u23[bool23][:N]
    return u01[:, 0], u01[:, 1], u23[:, 0], u23[:, 1]


def PickRandomPoint(u0, u1, u2, u3):
    x0 = u0
    x1 = u1
    x2 = u2 * ((1 - u0**2 - u1**2) / (u2**2 + u3**2))**0.5
    x3 = u3 * ((1 - u0**2 - u1**2) / (u2**2 + u3**2))**0.5
    return np.c_[x0, x1, x2, x3]


def RotationMatrix(x):
    M = np.array(
        [[1 - 2 * (x[1] * x[1] + x[2] * x[2]),
          2 * (x[0] * x[1] - x[3] * x[2]),
          2 * (x[0] * x[2] + x[3] * x[1])],
         [2 * (x[0] * x[1] + x[3] * x[2]),
          1 - 2 * (x[0] * x[0] + x[2] * x[2]),
          2 * (x[1] * x[2] - x[3] * x[0])],
         [2 * (x[0] * x[2] - x[3] * x[1]),
          2 * (x[1] * x[2] + x[3] * x[0]),
          1 - 2 * (x[0] * x[0] + x[1] * x[1])]]
    )
    return M
u0, u1, u2, u3 = get_randU(N=5)
x = PickRandomPoint(u0, u1, u2, u3)
RM = RotationMatrix(x[0])
#test
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.gca(projection='3d')
N=5000
S=np.random.rand(N,3)
S[:,1]*=0.4
S[:,2]*=0.2
S1=np.dot(S,RM)
x=S[:,0]
y=S[:,1]
z=S[:,2]
x1=S1[:,0]
y1=S1[:,1]
z1=S1[:,2]

ax.plot(x, y, z, 'k.', zdir='z', label='curve in (x,y)')
ax.plot(x1, y1, z1, 'r.', zdir='z', label='curve in (x,y)')
ax.set_xlim(-1, 1.3)
ax.set_ylim(-1, 1.3)
ax.set_zlim(-1, 1.3)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

print S
