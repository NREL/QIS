import matplotlib

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class PlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.canvas = FigureCanvasQTAgg(Figure())

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes_main = self.canvas.figure.add_subplot()

        self.setLayout(vertical_layout)