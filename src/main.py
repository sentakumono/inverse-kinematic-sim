# A test for a 2D kinematic arm. Its destination is randomized within its range so you can watch it struggle endlessly.

from matplotlib.pyplot import *
from math import *
from random import random
from numpy import linspace
from InvKin import Arm


fig = figure(figsize=(10, 10))
sp = fig.add_subplot(111)
sp.set_aspect('equal')

sp.plot((-15, 15), (-10, 10), c="#FFFFFF")


def set_destination():
    return int(20 * random() - 10), int(20 * random() - 10)


# destination = set_destination()
destination = (-5, -5)
dest_point, = sp.plot((-15, 15), [destination[1], destination[1]], marker="o", markersize=3)

arm_coord = 5
arm_L = sqrt(2 * (arm_coord ** 2))

arm_calc = Arm(arm_L, arm_L, destination)
# arm_calc_2 = Arm(arm_L, arm_L, (5, -5), (5, 5))


arm1 = arm_calc.graph(sp)
# arm2 = arm_calc_2.graph(sp)

# body, =   sp.plot(arm_calc.o, arm_calc_2.o)

tip = (0, 0)
distance = 1
# distance_2 = 1

while True:
    if distance < 0.2:
    # if (distance < 0.2) or (distance_2 < 0.2):
        destination = set_destination()
        # destination = (destination[0] + 0.1 if destination[0] < 5 else -1 * 0.5, -5)
        dest_point.set_xdata([destination[0]])
        dest_point.set_ydata([destination[1]])
        arm_calc.dest = destination
        # arm_calc_2.dest = destination
        #
        # delta = 0.05 if arm_calc.o[0] < 2 else 0
        # arm_calc.o = (arm_calc.o[0] + delta, arm_calc.o[1])
        # arm_calc_2.o = (arm_calc_2.o[0] + delta, arm_calc_2.o[1])
        # body.set_xdata([arm_calc.o[0], arm_calc_2.o[0]])
        # body.set_ydata([arm_calc.o[1], arm_calc_2.o[1]])



    distance = arm_calc.update(distance, arm1[0], arm1[1], arm1[2])
    # distance_2 = arm_calc_2.update(distance_2, arm2[0], arm2[1], arm2[2])

    draw()
    pause(0.01)

show()
