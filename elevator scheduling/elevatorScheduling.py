from PyQt5 import QtWidgets, QtGui, QtCore, uic
from Ui import Ui_MainWindow
import sys
from Schedul import elevator_schedul


#电梯1第一层坐标（350,800）
#电梯1坐标楼层换算（350,840-40*location[1]）


class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.schedul = elevator_schedul(self.ui)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()
    sys.exit(app.exec_())
