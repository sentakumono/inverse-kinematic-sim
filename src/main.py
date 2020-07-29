# The graph for the 3D quadraped bot
from matplotlib.pyplot import *
from mpl_toolkits import mplot3d as mp
from math import *
from numpy import linspace
from body import Body


if __name__ == "__main__":
    fig = figure(figsize=(9, 7))
    sp = mp.Axes3D(fig)

    sp.plot((-9, 9), (0, 0), (0, 0), c="#999999")
    sp.plot((0, 0), (-9, 9), (0, 0), c="#999999")
    sp.plot((0, 0), (0, 0), (0, 15), c="#999999")
    sp.text(9, 0, 0, 'x'), sp.text(0, 9, 0, "y"), sp.text(0, 0, 15, "z")


    body = Body(5, 8, 5)
    body.graph(sp)


    # translate corners to go in a circle in each plane
    del_x, del_y, del_z = [], [], []
    for x in np.linspace(0, 10*pi, 1000):
        del_x += [cos(x) / 30]
        del_y += [sin(x) / 30]
        del_z += [-sin(x) / 30]

    x, y, z = iter(del_x), iter(del_y), iter(del_z)

    pan, roll = 0, 0
    while True:
        # angles.set_text("\U000003B1: "+ str(int(degrees(arm_calc.a))) + ", \U000003B2: " + str(int(degrees(arm_calc.b))) + ", \U000003B3: " + str(int(degrees(arm_calc.c))))
        body.update(sp)
        body.translate([next(x), next(y), next(z)])
        # body.rotate([0.005, 0.005, 0.005])
        # pan, roll = sp.elev, sp.azim
        body.rotate_about_point([0.05, 0, 0], [0, 0, body.h])

        draw()
        pause(0.01)

