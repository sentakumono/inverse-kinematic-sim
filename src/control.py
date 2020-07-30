from PyQt5.Qt3DCore import QEntity, QTransform
from PyQt5.Qt3DExtras import QCuboidMesh, Qt3DWindow, QPhongMaterial, QTorusMesh, QOrbitCameraController
from PyQt5.Qt3DRender import QCamera

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QVector3D, QColor

import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import mpl_toolkits.mplot3d as mp
import matplotlib.pyplot as plt

from math import *
from body import Body


class mpl_canvas(FigureCanvasQTAgg):
    def __init__(self):
        fig = plt.figure(figsize=(9, 7))
        self.sp = mp.Axes3D(fig)
        super(mpl_canvas, self).__init__(fig)

    def initialize_graph(self):
        self.sp.plot((-9, 9), (0, 0), (0, 0), c="#999999")
        self.sp.plot((0, 0), (-9, 9), (0, 0), c="#999999")
        self.sp.plot((0, 0), (0, 0), (0, 15), c="#999999")
        self.sp.text(9, 0, 0, 'x'), self.sp.text(0, 9, 0, "y"), self.sp.text(0, 0, 15, "z")

    def create_body(self):
        body = Body(5, 8, 5)
        body.graph(self.sp)
        return body


class Control():
    def __init__(self):
        self.camera = QCamera()

    def createScene(self):
        root = QEntity()
        # Material
        material = QPhongMaterial(root)
        material.setAmbient(QColor(100, 100, 0))
        material.setDiffuse(QColor(100, 0, 100))

        cube_E = QEntity(root)
        cube_mesh = QCuboidMesh()
        cube_mesh.setXExtent(2)
        cube_mesh.setYExtent(2)
        cube_mesh.setZExtent(2)

        cube_tr = QTransform()
        cube_tr.setScale3D(QVector3D(2, 2, 2))

        cube_E.addComponent(cube_mesh)
        cube_E.addComponent(cube_tr)
        cube_E.addComponent(material)

        return root

    # def update_view(self, pan, roll):
    #     self.camera.panAboutViewCenter(pan)
    #     self.camera.roll(roll)

    def create_window(self):
        app = QApplication(sys.argv)
        view = Qt3DWindow()
        view.setTitle("Inverse Kinematic Controls")
        scene = self.createScene()
        #
        # fig = mpl_canvas()
        # fig.initialize_graph()
        # bot = fig.create_body()
        # # bot.graph(fig.sp)
        # bot.update(fig.sp)
        # fig.draw()

        self.camera = view.camera()
        self.camera.lens().setPerspectiveProjection(30, 4.0 / 3.0, 0.1, 1000.0)
        self.camera.setPosition(QVector3D(0, 0, 40.0))
        self.camera.setViewCenter(QVector3D(1., 1., 1.))

        # For camera controls
        camController = QOrbitCameraController(scene)
        camController.setLinearSpeed(25.0)
        camController.setLookSpeed(90.0)
        camController.setCamera(self.camera)

        view.setRootEntity(scene)
        view.show()
        # fig.show()
        app.exec_()


if __name__ == "__main__":
    # app = QApplication(sys.argv)
    con = Control()
    con.create_window()
    # app.exec_()
