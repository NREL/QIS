import matplotlib

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.canvas = FigureCanvasQTAgg(Figure())

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes_left = self.canvas.figure.add_subplot(221)
        self.canvas.axes_right = self.canvas.figure.add_subplot(222)
        self.canvas.axes_lower = self.canvas.figure.add_subplot(212)

        self.setLayout(vertical_layout)
