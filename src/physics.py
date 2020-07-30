# creates an object that tracks acceleration, velocity, and forces
class PhysicsObject():
    def __init__(self, mass=0, accel=[0, 0, -1]):
        self.m = mass
        self.a = accel
        self.v = [0, 0, 0]
        self.f = self.m * self.a

    # returns the centre of mass of a set of points
    def com(self, points):
        com = [0] * len(points[0])
        for i in range(len(points)):
            for j in range(len([com])):
                com[j] += points[i][j]

        com = [a / len(points) for a in com]

        return com

    # returns the resultant vector from summing the components of each given vector
    def resultant(self, f):
        comp = [*map(list, zip(*f))]
        r = [0] * len(comp)
        for i, e in enumerate(comp):
            r[i] = sum(e)
        return r

    def update(self):
        self.v = [a + b for a, b in zip(self.v, self.a)]


if __name__ == "__main__":
    phys = PhysicsObject()

    r = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # r = [[-1, 1, -1], [1, -1, 1]]

    print(phys.resultant(r))
    print(phys.com([[-1, 1], [1, -1], [1, 1], [-1, -1]]))
