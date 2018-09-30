import numpy as np

poses = np.load('poses-pullups3.npy')

poses = np.array([x[0] for x in poses])

"""Plot the 3D pose showing the joint connections."""
import matplotlib.pyplot as plt

import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.animation import FuncAnimation

def joint_color(j):
    """
    TODO: 'j' shadows name 'j' from outer scope
    """
    colors = [(0, 0, 0,1), (255, 0, 255,1), (0, 0, 255,1),
              (0, 255, 255,1), (255, 0, 0,1), (0, 255, 0,1)]
    _c = 0
    if j in range(1, 4):
        _c = 1
    if j in range(4, 7):
        _c = 2
    if j in range(9, 11):
        _c = 3
    if j in range(11, 14):
        _c = 4
    if j in range(14, 17):
        _c = 5
    return colors[_c]

#assert (pose.ndim == 2)
#assert (pose.shape[0] == 3)

for i in range(poses.shape[2]):
    plt.plot(range(poses.shape[0]),poses[:,0,i],color = joint_color(i),label = str(i) + 'x')
    plt.plot(range(poses.shape[0]),poses[:,1,i],color = joint_color(i),label = str(i) + 'y')
    plt.plot(range(poses.shape[0]),poses[:,2,i],color = joint_color(i),label = str(i) + 'z')
    plt.show()

plt.legend()
plt.show()





