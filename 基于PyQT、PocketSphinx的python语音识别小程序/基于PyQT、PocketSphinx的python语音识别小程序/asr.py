from PyQt5 import QtWidgets, QtGui, QtCore, uic

from asrInterface import Ui_MainWindow
import sys
import re
import threading

import speech_recognition as sr

import win32api

class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.recognize_btn.clicked.connect(self.listen_thread)#语音识别按钮连接监听线程
        self.ui.sphinx_bar.triggered.connect(self.sphinxbar_recognize)#sphinx模式触发
        self.ui.google_bar.triggered.connect(self.googlebar_recognize)#google模式触发
        self.ui.text_btn.clicked.connect(self.text_thread)#文本框输入确认按钮连接文本处理线程
        self.isgoogle = False#标志是否选择google识别API

    # sphinx从未选状态转变为已选状态时会触发sphinxbar_recognize函数
    def sphinxbar_recognize(self):
        self.ui.sphinx_bar.setChecked(True)
        self.ui.google_bar.setChecked(False)
        self.ui.label.setText("You change the API to sphinx.")
        self.ui.sphinx_action.setText(" √  sphinx  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.ui.sphinx_action.setFont(font)
        self.ui.sphinx_action.setStyleSheet(
            "QLabel { color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(50,50,50)\
                }"
            "QLabel:hover{ color: rgb(225,225,225);  /*字体颜色*/ \
                            background-color:rgb(0,117,210)\
                            }"
        )
        self.ui.google_action.setText("     google  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.ui.google_action.setFont(font)
        self.ui.google_action.setStyleSheet(
            "QLabel { color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(50,50,50)\
                }"
            "QLabel:hover{ color: rgb(225,225,225);  /*字体颜色*/ \
                            background-color:rgb(0,117,210)\
                            }"
        )
        self.isgoogle = False

    # google从未选状态转变为已选状态时会触发googlebar_recognize函数
    def googlebar_recognize(self):
        self.ui.google_bar.setChecked(True)
        self.ui.sphinx_bar.setChecked(False)
        self.ui.label.setText("You change the API to google.")
        self.ui.sphinx_action.setText("     sphinx  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.ui.sphinx_action.setFont(font)
        self.ui.sphinx_action.setStyleSheet(
            "QLabel { color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(50,50,50)\
                }"
            "QLabel:hover{ color: rgb(225,225,225);  /*字体颜色*/ \
                            background-color:rgb(0,117,210)\
                            }"
        )
        self.ui.google_action.setText(" √  google  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.ui.google_action.setFont(font)
        self.ui.google_action.setStyleSheet(
            "QLabel { color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(50,50,50)\
                }"
            "QLabel:hover{ color: rgb(225,225,225);  /*字体颜色*/ \
                            background-color:rgb(0,117,210)\
                            }"
        )
        self.isgoogle = True

    #创建文本处理线程
    def text_thread(self):
        t2 = threading.Thread(target=self.text_changed)
        t2.setDaemon(True)
        t2.start()
    #文本处理函数
    def text_changed(self):
        content = self.ui.textbox.text()
        print(content)
        COMMEND = ["music", "readme"]
        commend_is_music = re.search(COMMEND[0].lower(), content.lower())
        commend_is_file = re.search(COMMEND[1].lower(), content.lower())
        if commend_is_music:
            self.ui.label.setText("You typed: \" " + content + "\"")
            win32api.ShellExecute(0, 'open', '音乐文件\\好久不见.mp3', '', '', 1)
        elif commend_is_file:
            self.ui.label.setText("You typed: \"" + content + "\"")
            win32api.ShellExecute(0, 'open', 'readme\\readme.pdf', '', '', 0)
        else:
            self.ui.label.setText("You typed: \" " + content + "\"\nIt's not a valid command.")

    #创建监听函数
    def listen_thread(self):
        self.ui.label.setText("I'm listening...... ")
        t1 = threading.Thread(target=self.listen)
        t1.setDaemon(True)
        t1.start()

    #声音识别及处理函数
    def listen(self):
        # Working with Microphones
        mic = sr.Recognizer()
        with sr.Microphone() as source:  # use the default microphone as the audio source
            audio = mic.listen(source)  # listen for the first phrase and extract it into audio data
        try:
            if self.isgoogle:
                content = mic.recognize_google(audio)
            else:
                content = mic.recognize_sphinx(audio)
        except sr.RequestError:
            self.ui.label.setText("Something was wrong! Try again......")

        COMMEND = ["music", "readme"]
        commend_is_music = re.search(COMMEND[0].lower(), content.lower())
        commend_is_file = re.search(COMMEND[1].lower(), content.lower())
        if commend_is_music:
            self.ui.label.setText("You said: \" " + content + "\"")
            win32api.ShellExecute(0, 'open', '音乐文件\\好久不见.mp3', '', '', 1)
        elif commend_is_file:
            self.ui.label.setText("You said: \"" + content + "\"")
            win32api.ShellExecute(0, 'open', 'readme\\readme.pdf', '', '', 0)
        else:
            self.ui.label.setText("You said: \" " + content + "\"\nIt's not a valid command.")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()
    sys.exit(app.exec_())


