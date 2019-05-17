from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 900)
        MainWindow.setStyleSheet("#MainWindow{border-image:url(icon/background5.png)}")
        self.Wwidget = QtWidgets.QWidget(MainWindow)
        self.Wwidget.resize(700, 900)

        self.upbtn_style = "QPushButton{border-image: url(icon/up_hover.png)}"\
            "QPushButton:hover{border-image: url(icon/up.png)}"\
            "QPushButton:pressed{border-image: url(icon/up_pressed.png)}"
        self.downbtn_style = "QPushButton{border-image: url(icon/down_hover.png)}" \
            "QPushButton:hover{border-image: url(icon/down.png)}" \
            "QPushButton:pressed{border-image: url(icon/down_pressed.png)}"

        self.elevator_label = {}
        for i in range(1, 6):
            self.elevator_label[i] = QtWidgets.QLabel(MainWindow)
            self.elevator_label[i].setPixmap(QtGui.QPixmap("icon/elevator.png"))
            self.elevator_label[i].setGeometry(QtCore.QRect(i*100 - 92.5, 862.5, 35, 35))
            self.elevator_label[i].setScaledContents(True)

        self.location_label = {}
        for i in range(1, 6):
            self.location_label[i] = QtWidgets.QLabel(MainWindow)
            self.location_label[i].setText("1")
            self.location_label[i].setGeometry(QtCore.QRect(i * 100 - 70, 20, 80, 40))
            font = QtGui.QFont()
            font.setFamily("Calibri")
            font.setPointSize(40)
            font.setStyleStrategy(QtGui.QFont.PreferAntialias)
            self.location_label[i].setFont(font)
            self.location_label[i].setStyleSheet("color: rgb(217, 104, 49);")
            self.location_label[i].setTextFormat(QtCore.Qt.AutoText)
            self.location_label[i].setWordWrap(True)
        '''
        self.isup_label = {}
        self.isdown_label = {}
        for i in range(1, 6):
            self.isup_label[i] = QtWidgets.QLabel(MainWindow)
            self.isdown_label[i] = QtWidgets.QLabel(MainWindow)
            self.isup_label[i].setPixmap(QtGui.QPixmap("icon/isnotup.png"))
            self.isdown_label[i].setPixmap(QtGui.QPixmap("icon/isnotdown.png"))
            self.isup_label[i].setGeometry(QtCore.QRect(i*100 - 70, 70, 20, 20))
            self.isdown_label[i].setGeometry(QtCore.QRect(i * 100 - 40, 70, 20, 20))
            self.isdown_label[i].setScaledContents(True)
            self.isup_label[i].setScaledContents(True)
        '''
        self.elevator_Anim = {}
        for i in range(1, 6):
            self.elevator_Anim[i] = QtCore.QPropertyAnimation(self.elevator_label[i], b"geometry")

        self.up_btn = {}
        for i in range(1, 20):
            self.up_btn[i] = QtWidgets.QPushButton(MainWindow)  # 创建一个按钮，并将按钮加入到窗口MainWindow中
            self.up_btn[i].setGeometry(QtCore.QRect(507.5, 902.5 - i * 40, 35, 35))
            self.up_btn[i].setStyleSheet(self.upbtn_style)

        self.down_btn = {}
        for i in range(2, 21):
            self.down_btn[i] = QtWidgets.QPushButton(MainWindow)  # 创建一个按钮，并将按钮加入到窗口MainWindow中
            self.down_btn[i].setGeometry(QtCore.QRect(557.5, 902.5 - i * 40, 35, 35))
            self.down_btn[i].setStyleSheet(self.downbtn_style)

        self.number_btn = [[]for i in range(6)]  # 为使索引序号与电梯序号对应起来，创建六个子数组，第0个不加操作
        for i in range(1, 6):
            self.number_btn[i].append(0)  # 为使索引序号与电梯楼层对应起来，在第0个位置添加空项，用0替代
            for j in range(1, 21):
                self.number_btn[i].append(QtWidgets.QPushButton(MainWindow))  # 创建一个按钮，并将按钮加入到窗口MainWindow中
                self.number_btn[i][j].setGeometry(QtCore.QRect(i*100-42.5, 902.5 - j * 40, 35, 35))
                self.number_btn[i][j].setStyleSheet(
                    "QPushButton{border-image: url(icon/"+str(j)+"_hover.png)}"
                    "QPushButton:hover{border-image: url(icon/"+str(j)+".png)}"
                    "QPushButton:pressed{border-image: url(icon/"+str(j)+"_pressed.png)}"
                    )

def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "anim"))
