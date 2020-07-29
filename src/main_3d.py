# The graph for the 3D quadraped bot
from matplotlib.pyplot import *
from mpl_toolkits import mplot3d as mp
from math import *
from numpy import linspace
from InvKin import Arm3D
from body import Body
# from control import Control

fig = figure(figsize=(9, 7))
sp = mp.Axes3D(fig)

sp.plot((-9, 9), (0, 0), (0, 0), c="#999999")
sp.plot((0, 0), (-9, 9), (0, 0), c="#999999")
sp.plot((0, 0), (0, 0), (0, 15), c="#999999")
sp.text(9, 0, 0, 'x'), sp.text(0, 9, 0, "y"), sp.text(0, 0, 15, "z")

# controls = Control()
# fig, sp = controls.mpl_canvas()

body = Body(5, 8, 5)
body.graph(sp)

# controls.create_window()
# translate corners to go in a circle in each plane
del_x, del_y, del_z = [], [], []
for x in np.linspace(0, 10*pi, 1000):
    del_x += [cos(x) / 60]
    del_y += [sin(x) / 60]
    del_z += [-sin(x) / 60]

x, y, z = iter(del_x), iter(del_y), iter(del_z)

pan, roll = 0, 0
while True:
    # angles.set_text("\U000003B1: "+ str(int(degrees(arm_calc.a))) + ", \U000003B2: " + str(int(degrees(arm_calc.b))) + ", \U000003B3: " + str(int(degrees(arm_calc.c))))
    print("a")
    body.update(sp)
    # body.translate([next(x), next(y), next(z)])
    body.rotate([0.005, 0.005, 0.005])
    # pan, roll = sp.elev, sp.azim
    # controls.update_view(pan, roll)
    draw()
    pause(0.01)

