import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 messagebox - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

    def lockin_error_window(self, error_message):
        print('Trying to generate error_message_window')
        # error_message_window('WARNING - Lock-in Status Issues',
        #                      inform_text='Something is wrong with the lockin.\n LIAS? Response is: '
        #                                  + str(error_message) + '\nContinue Anyway?')

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText('Lock-in Status Register Flagged Issue(s)')
        msg.setInformativeText('One or more lock-in issues are present which may affect your results.\n'
                               'LIA Status Register Value is: ' + str(error_message) + '\n\nContinue Anyway?')
        msg.setWindowTitle(' - Warning - ')
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Abort)
        # msg.buttonClicked.connect(msgbtn)
        return_value = msg.exec()
        print('msg.clickedButton(): ' + str(msg.clickedButton()))
        print('msg box return value: ' + str(return_value))
        if return_value == QMessageBox.Abort:
            print('Abort pressed')
        elif return_value == QMessageBox.Ok:
            print('OK pressed')

    def print_test(self):
        print('test')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.lockin_error_window(3)
    sys.exit(app.exec_())


x = 1
y = 2
z = 3
t0 = time.time()
for ii in range(0, 1000000):
    if x == y and not x == z:
        test_str = 'heres ' + 'a' + ' string!1'
    elif not x == y and x == z:
        test_str = 'heres ' + 'a' + ' string!2'
    elif x == y and x == z:
        test_str = 'heres ' + 'a' + ' string!3'
    elif not x == y and not x == z:
        test_str = 'heres ' + 'a' + ' string!4'

print('duration' + str(time.time() - t0))
print('test string: ' + str(test_str))

x = 1
y = 2
z = 1
t0 = time.time()
for ii in range(0, 1000000):
    if x == y:
        test_str = 'heres ' + 'a' + ' string!1'
    elif not x == y:
        test_str = 'heres ' + 'a' + ' string!NOT'

    if x == z:
        test_str = 'rewrite!'

print('duration' + str(time.time() - t0))
print('test string: ' + str(test_str))