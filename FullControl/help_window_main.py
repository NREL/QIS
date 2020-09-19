import os
import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget

from FullControl.help_window_ui import Ui_Form as Help_Ui_Form

pyqt = os.path.dirname(PyQt5.__file__)  # This and the following line are essential to make guis run
QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))


class HelpWindowForm(QWidget):
    def __init__(self, *args, **kwargs):
        super(HelpWindowForm, self).__init__(*args, **kwargs)

        # Load the ui.py file and prepare the UI
        self.ui = Help_Ui_Form()
        self.ui.setupUi(self)


# ------------------------------------------------ RUN THE PROGRAM -----------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Defines the instance of the whole application
    app.setStyle('Fusion')
    help_window = HelpWindowForm()  # Declares the instance of the main window class
    # This ^ is where the gui is prepared before being presented in the next line\/
    help_window.show()
    sys.exit(app.exec_())
