# A test for a 2D kinematic arm. Its destination is randomized within its range so you can watch it struggle endlessly.

from matplotlib.pyplot import *
from math import *
from random import random


# Model for a 2D kinematic arm.
class Arm:
    def __init__(self, a_len, b_len, dest, origin=(0, 0), angles=(7 / 4 * pi, pi)):
        self.a_l = a_len
        self.b_l = b_len
        self.dest = dest

        self.a = angles[0]
        self.b = angles[1]

        self.o = origin

        self.prev_gra = 0
        self.prev_grb = 0

    # calculate distance between tip and destination, theta added to determine possible movements
    def calc_dist(self, theta_a=0.0, theta_b=0.0):
        tip = (self.a_l * cos(self.a + theta_a) + self.b_l * cos(self.b + theta_b) + self.o[0]), \
              (self.a_l * sin(self.a + theta_a) + self.b_l * sin(self.b + theta_b) + self.o[1])
        distance = sqrt((tip[0] - self.dest[0]) ** 2 + (tip[1] - self.dest[1]) ** 2)

        return distance

    # returns distance from tip to line
    def calc_dist_plane(self, theta_a=0.0, theta_b=0.0):
        tip = (self.a_l * cos(self.a + theta_a) + self.b_l * cos(self.b + theta_b) + self.o[0]), \
              (self.a_l * sin(self.a + theta_a) + self.b_l * sin(self.b + theta_b) + self.o[1])
        distance = tip[1] - self.dest[1]

        return distance

    #
    def find_angle(self, a, b, theta=1.0):
        theta = radians(theta)

        gradient_a = self.calc_dist(theta, 0) - self.calc_dist(-theta, 0)
        gradient_b = self.calc_dist(0, theta) - self.calc_dist(0, -theta)

        speed_a, speed_b = 0, 0
        if abs(gradient_a) + abs(self.prev_gra) < gradient_a + self.prev_gra and not isclose(gradient_a, self.prev_gra):
            a -= speed_a * (self.prev_gra / (gradient_a - self.prev_gra))
            speed_a = 0
        else:
            speed_a += gradient_a

        if abs(gradient_b) + abs(self.prev_grb) < gradient_b + self.prev_grb and not isclose(gradient_b, self.prev_grb):
            b -= speed_b * (self.prev_grb / (gradient_b - self.prev_grb))
            speed_b = 0
        else:
            speed_b += gradient_b

        a -= speed_a
        b -= speed_b

        self.prev_gra = gradient_a
        self.prev_grb = gradient_b
        return a, b

    # functions for updating the graph
    def graph(self, sp):
        arm1, = sp.plot((self.o[0], self.a_l), (self.o[1], self.a_l))
        joint_a = sp.plot([self.o[0]], [self.o[1]], marker="o", markersize=5)
        joint_b, = sp.plot([self.o[0]], [self.o[1]], marker="o", markersize=5)
        arm2, = sp.plot((self.a_l, self.b_l), (self.a_l, self.b_l))
        return [arm1, arm2, joint_b]

    # animating the arm movement
    def update(self, distance, arm1, arm2, joint_b):
        self.a, self.b = self.find_angle(self.a, self.b, 0.5 / ((self.a_l + self.b_l) / 2) if distance < 0.5 else 2.5 / ((self.a_l + self.b_l) / 2))
        distance = self.calc_dist()

        joint = (self.a_l * cos(self.a) + self.o[0]), (self.a_l * sin(self.a) + self.o[1])
        tip = (self.b_l * cos(self.b) + joint[0]), (self.b_l * sin(self.b) + joint[1])

        joint_b.set_xdata([joint[0]])
        joint_b.set_ydata([joint[1]])
        arm1.set_xdata((self.o[0], joint[0]))
        arm1.set_ydata((self.o[1], joint[1]))
        arm2.set_xdata((joint[0], tip[0]))
        arm2.set_ydata((joint[1], tip[1]))

        return distance


if __name__ == "__main__":
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
