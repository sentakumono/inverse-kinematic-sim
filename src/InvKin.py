from math import *
import numpy as np

# Model for a 2D kinematic arm. The 3D one is cooler go look at that instead
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


# model for a 3D kinematic arm with 1 DOF at its centre joint and 2 at its base
class Arm3D:
    def __init__(self, a_len, b_len, dest, origin=(0, 0, 0), angles=(-3/4 * pi,-pi/4, 0)):
        self.a_l = a_len
        self.b_l = b_len
        self.dest = dest
        self.o = origin
        self.distance = 1

        self.a, self.b, self.c = angles
        self.prev_gr = [0, 0, 0]

    # helper, returns the location of the leg's tip
    def get_tip(self) -> tuple:
        tip = (self.a_l * sin(self.c) + self.b_l * sin(self.c) + self.o[0]), \
              (self.a_l * cos(self.a) + self.b_l * cos(self.b) + self.o[1]), \
              (self.a_l * sin(self.a) + self.b_l * sin(self.b) + self.o[2])

        return tip

    # calculate distance between tip and destination, theta added to determine possible movements
    def calc_dist(self, theta_a=0.0, theta_b=0.0, theta_c=0.0) -> float:
        # tip = (self.a_l * cos(self.a + theta_a) + self.b_l * cos(self.b + theta_b) + self.o[0]), \
        #       (self.a_l * sin(self.a + theta_a) + self.b_l * sin(self.b + theta_b) + self.o[1]), \
        #       (self.a_l * sin(self.c + theta_c) + self.b_l * sin(self.c + theta_c) + self.o[2])
        tip = (self.a_l * sin(self.c + theta_c) + self.b_l * sin(self.c + theta_c) + self.o[0]), \
              (self.a_l * cos(self.a + theta_a) + self.b_l * cos(self.b + theta_b) + self.o[1]), \
              (self.a_l * sin(self.a + theta_a) + self.b_l * sin(self.b + theta_b) + self.o[2])
        distance = sqrt((tip[0] - self.dest[0]) ** 2 + (tip[1] - self.dest[1]) ** 2 + (tip[2] - self.dest[2]) ** 2)

        return distance

    # Find the change in angle that brings the tip of the arm closer
    # to the destination by comparing small changes to each angle
    # in either direction
    def find_angle(self, angle, theta=1.0) -> list:
        theta = radians(theta)
        gradients = [self.calc_dist(theta, 0, 0) - self.calc_dist(-theta, 0, 0),
                     self.calc_dist(0, theta, 0) - self.calc_dist(0, -theta, 0),
                     self.calc_dist(0, 0, theta) - self.calc_dist(0, 0, -theta)]

        #   This version is faster but more unstable
        # for i in range(len(gradients)):
        #     # if the gradients are opposite signs (past destination), slow it down towards the opposite direction & reset
        #     if abs(gradients[i]) + abs(self.prev_gr[i]) > abs(gradients[i] + self.prev_gr[i]) and not isclose(gradients[i], self.prev_gr[i]):
        #         angle[i] -=  self.speed[i] * (self.prev_gr[i] / (gradients[i] - self.prev_gr[i]))
        #         self.speed[i] = 0
        #     else:
        #         self.speed[i] += gradients[i]
        #     angle[i] -= self.speed[i]

        # real python moment
        for i in range(len(gradients)):
            # if the gradients are opposite signs (past destination), slow it down towards the opposite direction & reset
            angle[i] -= gradients[i] * (-1 if np.sign(gradients[i]) != np.sign(self.prev_gr[i]) and not isclose(gradients[i], self.prev_gr[i]) else 1)

        self.prev_gr = gradients
        return angle

    # def add_transformation(self, t):
    #     self.t = [a + b for a, b in zip(self.t, t)]
    #     self.dest = [a - b for a, b in zip(self.dest, t)]

    # initialize graph objects
    def graph(self, sp) -> list:
        arm1, = sp.plot((self.o[0], sqrt(3 * self.a_l ** 2)), (self.o[1], 0), (self.o[2], 0), c="#999999")
        joint_a, = sp.plot([self.o[0]], [self.o[1]], [self.o[2]], marker="o", markersize=5, c="#555599")
        joint_b, = sp.plot([self.o[0]], [self.o[1]], [self.o[2]], marker="o", markersize=5, c="#555599")
        arm2, = sp.plot((sqrt(3 * self.a_l ** 2), sqrt(3 * self.b_l ** 2)), (0, 0), (0, 0), c="#999999")

        return [arm1, arm2, joint_a, joint_b]


    # animate graph objects
    def update(self, arm):
        # determine speed angle should change at depending on distance and arm length
        speed =  0.2 / ((self.a_l + self.b_l) / 2) if self.distance < 0.5 else 2 / ((self.a_l + self.b_l) / 2)
        self.a, self.b, self.c = self.find_angle([self.a, self.b, self.c], speed)
        self.distance = self.calc_dist()

        # determine the location of the central joint and tip of the arm
        # joint = (self.a_l * cos(self.a) + self.o[0]), (self.a_l * sin(self.a) + self.o[1]), (self.a_l * sin(self.c) + self.o[2])
        # tip = (self.b_l * cos(self.b) + joint[0]), (self.b_l * sin(self.b) + joint[1]), (self.b_l * sin(self.c) + joint[2])
        joint = (self.a_l * sin(self.c) + self.o[0]), (self.a_l * cos(self.a) + self.o[1]), (self.a_l * sin(self.a) + self.o[2])
        tip = (self.b_l * sin(self.c) + joint[0]), (self.b_l * cos(self.b) + joint[1]), (self.b_l * sin(self.b) + joint[2])

        arm1, arm2, joint_a, joint_b = arm
        joint_a.set_xdata([self.o[0]])
        joint_a.set_ydata([self.o[1]])
        joint_a.set_3d_properties([self.o[2]])
        joint_b.set_xdata([joint[0]])
        joint_b.set_ydata([joint[1]])
        joint_b.set_3d_properties([joint[2]])
        arm1.set_xdata((self.o[0], joint[0]))
        arm1.set_ydata((self.o[1], joint[1]))
        arm1.set_3d_properties((self.o[2], joint[2]))
        arm2.set_xdata((joint[0], tip[0]))
        arm2.set_ydata((joint[1], tip[1]))
        arm2.set_3d_properties((joint[2], tip[2]))

