# The graph for the 3D quadraped bot

from matplotlib.pyplot import *
from mpl_toolkits import mplot3d as mp
from math import *
from random import random
from numpy import linspace
from InvKin import Arm3D
from body import Body

fig = figure(figsize=(10, 10))
sp = mp.Axes3D(fig)

# sp.set_aspect('equal')

sp.plot((-9, 9), (0, 0), (0, 0), c="#999999")
sp.plot((0, 0), (-9, 9), (0, 0), c="#999999")
sp.plot((0, 0), (0, 0), (0, 15), c="#999999")
sp.text(9, 0, 0, 'x'), sp.text(0, 9, 0, "y"), sp.text(0, 0, 15, "z")


#
# def set_destination():
#     return int(20 * random() - 10), int(20 * random() - 10), int(20 * random() - 10)


# destination = set_destination()
# destination = (-5, -5, -5)
# dest_point, = sp.plot([destination[0]],[destination[1]], destination[2], marker="o", markersize=3)

# arm_coord = 5
# arm_L = sqrt(2 * (arm_coord ** 2))

# arm_calc = Arm3D(arm_L, arm_L, destination)
# arm_calc_2 = Arm3D(arm_L, arm_L, destination, (5, 5, 5))

# arm1 = arm_calc.graph(sp)
# arm2 = arm_calc_2.graph(sp)

# body, =   sp.plot(arm_calc.o, arm_calc_2.o)

body = Body(5, 8, 5)
body.graph(sp)

del_x, del_y, del_z = [], [], []
for x in np.linspace(0, 10*pi, 1000):
    del_x += [cos(x) / 20]
    del_y += [sin(x) / 20]
    del_z += [sin(x) / 15]

x, y, z = iter(del_x), iter(del_y), iter(del_z)

while True:
    # if distance < 0.2:

    # if (distance < 0.5) or (distance_2 < 0.5):
    #     destination = set_destination()
    #     dest_point.set_xdata([destination[0]])
    #     dest_point.set_ydata([destination[1]])
    #     dest_point.set_3d_properties([destination[2]])
    #     arm_calc.dest = destination
    #     # arm_calc_2.dest = destination
        # delta = -0.05 if arm_calc.o[0] < 2 else 0
        # arm_calc.o = (arm_calc.o[0] + delta, arm_calc.o[1] + delta)
        # arm_calc_2.o = (arm_calc_2.o[0] + delta, arm_calc_2.o[1] + delta)
        # body.set_xdata([arm_calc.o[0], arm_calc_2.o[0]])
        # body.set_ydata([arm_calc.o[1], arm_calc_2.o[1]])

    # distance = arm_calc.update(distance, arm1[0], arm1[1], arm1[2])
    # distance_2 = arm_calc_2.update(distance_2, arm2[0], arm2[1], arm2[2])
    # angles.set_text("\U000003B1: "+ str(int(degrees(arm_calc.a))) + ", \U000003B2: " + str(int(degrees(arm_calc.b))) + ", \U000003B3: " + str(int(degrees(arm_calc.c))))

    # Animate and rotate the body
    body.update(sp)
    # body.translate([next(x), next(y), next(z)])
    body.rotate(0, 0.01, 0)

    draw()
    pause(0.01)

show()
