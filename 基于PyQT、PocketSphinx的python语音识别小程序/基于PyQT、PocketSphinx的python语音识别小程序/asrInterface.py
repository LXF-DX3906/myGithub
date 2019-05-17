# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asrInterface.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(380, 700)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 添加菜单——模式按钮：可选sphinx模式或google模式
        self.menu_bar = QMainWindow.menuBar(MainWindow)
        self.model_bar = self.menu_bar.addMenu("Model")
        self.menu_bar.setFont(QtGui.QFont('Microsoft YaHei', 9))
        self.menu_bar.setStyleSheet(
            "QMenuBar::item { \
                font-size: 10pt; \
                color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(50,50,50)\
            } \
            QMenuBar::item:selected { \
                background-color:rgb(0,117,210);/*选中的样式*/ \
            } \
            QMenuBar::item:pressed {/*菜单项按下效果*/ \
                border: 1px solid rgb(60,60,61); \
                background-color: rgb(0,117,210); \
            } \
             "
        )

        # 向QMenu小控件中添加按钮，子菜单
        #sphinx模式按钮
        self.sphinx_bar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.sphinx_bar.setChecked(True)
        self.sphinx_action = QtWidgets.QLabel(" √  sphinx  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.sphinx_action.setFont(font)
        self.sphinx_action.setStyleSheet(
            "QLabel { color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(50,50,50)\
                }"
            "QLabel:hover{ color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(0,117,210)\
                }"
        )
        self.sphinx_bar.setDefaultWidget(self.sphinx_action)

        #google模式按钮
        self.google_bar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.google_bar.setChecked(False)
        self.google_action = QtWidgets.QLabel("     google  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.google_action.setFont(font)
        self.google_action.setStyleSheet(
            "QLabel { color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(50,50,50)\
                }"
            "QLabel:hover{ color: rgb(225,225,225);  /*字体颜色*/ \
                            background-color:rgb(0,117,210)\
                            }"
        )
        self.google_bar.setDefaultWidget(self.google_action)

        #将两按钮添加到model_bar中去
        self.model_bar.addAction(self.sphinx_bar)
        self.model_bar.addAction(self.google_bar)

        # 创建一个文本框，并将按钮加入到窗口MainWindow中
        self.textbox = QtWidgets.QLineEdit(MainWindow)
        self.textbox.setFont(QtGui.QFont('Microsoft YaHei', 15))
        self.textbox.setGeometry(40, 633, 300, 40)
        self.textbox.setStyleSheet(
            "QLineEdit{color:rgb(0,0,0)}"  # 按键前景色
            "QLineEdit{background-color:rgb(242,242,242)}"  # 按键背景色
            "QLineEdit:hover{background-color:rgb(255,255,255)}"  # 光标移动到上面后的前景色
        )

        # 创建文本框输入确认按钮，并将按钮加入到窗口MainWindow中
        self.text_btn = QtWidgets.QPushButton(MainWindow)
        self.text_btn.setFont(QtGui.QFont('Microsoft YaHei', 10))
        self.text_btn.setGeometry(340, 633, 40, 40)
        self.text_btn.setStyleSheet(
            "QPushButton{border-image: url(icon/search.png)}"
            "QPushButton:hover{border-image: url(icon/search3.png)}"
            "QPushButton:pressed{border-image: url(icon/search.png)}"
        )

        # 创建语音识别开始按钮，并将按钮加入到窗口MainWindow中
        self.recognize_btn = QtWidgets.QPushButton(MainWindow)  # 创建一个按钮，并将按钮加入到窗口MainWindow中
        self.recognize_btn.setFont(QtGui.QFont('Microsoft YaHei', 10))
        self.recognize_btn.setGeometry(0, 633, 40, 40)
        self.recognize_btn.setStyleSheet(
            "QPushButton{border-image: url(icon/phone3.png)}"
            "QPushButton:hover{border-image: url(icon/phone4.png)}"
            "QPushButton:pressed{border-image: url(icon/phone3.png)}"
        )

        #加载动态图片
        self.voiceFig = QtWidgets.QLabel(self.centralwidget)
        self.voiceFig.setGeometry(QtCore.QRect(28, 50, 322, 242))
        self.voiceFig.setText("")
        self.gif = QMovie("icon/voice.gif")
        self.voiceFig.setMovie(self.gif)
        self.gif.start()
        self.voiceFig.setScaledContents(True)
        self.voiceFig.setObjectName("voiceFig")

        # Hi! How can I help?
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 250, 300, 150))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 117, 210);")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        # You can:
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 450, 350, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 117, 210);")
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        # 1. Enjoy music by saying \"Play music\"
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 480, 350, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(0, 117, 210);")
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")

        # 2. Take some notes by saying \"Open Notepad\"
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 510, 350, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(0, 117, 210);")
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Voice Assistant"))
        self.label.setText(_translate("MainWindow", "Hi! How can I help?"))
        self.label_2.setText(_translate("MainWindow", "You can:"))
        self.label_3.setText(_translate("MainWindow", "1. Enjoy music by saying \"Play music\""))
        self.label_4.setText(_translate("MainWindow", "2. Take some notes by saying \"Open Notepad\""))


