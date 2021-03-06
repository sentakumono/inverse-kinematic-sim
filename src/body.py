from InvKin import Arm3D
from mpl_toolkits import mplot3d as mp
from math import *
from matplotlib.pyplot import *


# A quadrilateral body driving the origin points of 4 kinematic legs.
# Translations and rotations of the body will cause the legs to react.
class Body():
    def __init__(self, w, l, h, o=(0, 0, 0)):
        self.w = w
        self.l = l
        self.h = h
        self.o = o

        self.corners = np.array([(o[0] + w / 2, o[1] + l / 2, o[2] + h), (o[0] + w / 2, o[1] - l / 2, o[2] + h),
                                 (o[0] - w / 2, o[1] - l / 2, o[2] + h), (o[0] - w / 2, o[1] + l / 2, o[2] + h)])

        self.legs = [Arm3D(4, 4, (self.corners[0][0], self.corners[0][1], self.corners[0][2] - h), self.corners[0]),
                     Arm3D(4, 4, (self.corners[1][0], self.corners[1][1], self.corners[1][2] - h), self.corners[1]),
                     Arm3D(4, 4, (self.corners[2][0], self.corners[2][1], self.corners[2][2] - h), self.corners[2]),
                     Arm3D(4, 4, (self.corners[3][0], self.corners[3][1], self.corners[3][2] - h), self.corners[3])
                     ]
        self.leg_graphs = [[]] * 4
        self.leg_dist = [1] * 4
        self.rotation = [0] * 3

    # TODO: Transformations need limits so it doesn't crumple

    # translate the body by a given offset
    def translate(self, delta, lim=True):
        # temporary limit, need to make it based off of leg range
        for i in range(len(delta)):
            if delta[i] > 2 and lim:
                delta[i] = 0
        for i, corner in enumerate(self.corners):
            self.corners[i] = (corner[0] + delta[0], corner[1] + delta[1], corner[2] + delta[2])

    # rotate the body around the 3 axes
    def rotate(self, rot):
        # temporary limit, but may keep it as it seems physically reasonable
        for i in range(len(rot)):
            if self.rotation[i] >= pi / 6:
                rot[i] = 0
        x, y, z = rot
        # 3D rotation matrix for 3x1 corner point
        r_1, r_2, r_3 = np.array([[1, 0, 0], [0, cos(x), -sin(x)], [0, sin(x), cos(x)]]), \
                        np.array([[cos(y), 0, sin(y)], [0, 1, 0], [-sin(y), 0, cos(y)]]), \
                        np.array([[cos(z), -sin(z), 0], [sin(z), cos(z), 0], [0, 0, 1]])

        r = np.matmul(r_1, np.matmul(r_2, r_3))

        self.rotation = [a + b for a, b in zip([x, y, z], self.rotation)]
        # self.corners = np.matmul(self.corners, r)
        for i, e in enumerate(self.corners):
            self.corners[i] = np.matmul(e, r)

    # translate point to origin then apply rotation
    # kinda scuffed ngl
    def rotate_about_point(self, rot, point):
        self.translate([-a for a in point], False)
        self.rotate(rot)
        self.translate(point, False)

    # initialize graph objects
    def graph(self, sp):
        for i, leg in enumerate(self.legs):
            self.leg_graphs[i] = leg.graph(sp)
        body_graph = sp.add_collection3d(mp.art3d.Poly3DCollection([self.corners]))
        return body_graph

    # animate graph objects
    def update(self, sp):
        for i, leg in enumerate(self.legs):
            leg.update(self.leg_graphs[i])
            # self.legs[i].o = self.corners[i]
        sp.collections.pop()
        sp.add_collection3d(mp.art3d.Poly3DCollection([self.corners]), zs=self.corners[0][0])
