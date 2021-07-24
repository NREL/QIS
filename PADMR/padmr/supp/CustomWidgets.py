from PyQt5 import QtWidgets, QtCore
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

# class TestCustomDoubleSpinBox(QtWidgets.QDoubleSpinBox):
#     def __init__(self, *args):
#         super(TestCustomDoubleSpinBox, self).__init__(*args)


class CustomDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, *args):
        super(CustomDoubleSpinBox, self).__init__(*args)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def focusInEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        super(CustomDoubleSpinBox, self).focusInEvent(event)

    def focusOutEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        super(CustomDoubleSpinBox, self).focusOutEvent(event)

    def wheelEvent(self, event):
        if self.hasFocus():
            return super(CustomDoubleSpinBox, self).wheelEvent(event)
        else:
            event.ignore()


class CustomSpinBox(QtWidgets.QSpinBox):
    def __init__(self, *args):
        super(CustomSpinBox, self).__init__(*args)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def focusInEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        super(CustomSpinBox, self).focusInEvent(event)

    def focusOutEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        super(CustomSpinBox, self).focusOutEvent(event)

    def wheelEvent(self, event):
        if self.hasFocus():
            return super(CustomSpinBox, self).wheelEvent(event)
        else:
            event.ignore()


class CustomComboBox(QtWidgets.QComboBox):
    def __init__(self, *args):
        super(CustomComboBox, self).__init__(*args)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def focusInEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        super(CustomComboBox, self).focusInEvent(event)

    def focusOutEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        super(CustomComboBox, self).focusOutEvent(event)

    def wheelEvent(self, event):
        if self.hasFocus():
            return super(CustomComboBox, self).wheelEvent(event)
        else:
            event.ignore()