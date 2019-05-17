import threading
from functools import partial
import time
from PyQt5 import QtCore, QtGui
import sys


class elevator_schedul():
    def __init__(self, ui):
        self.ui = ui
        self.isUp = {}  # 电梯上行标志数组
        self.isDown = {}  # 电梯下行标志数组
        self.last_isUp = {}  # 电梯前一次上行标志数组
        self.last_isDown = {}  # 电梯前一次下行标志数组
        self.location = {}  # 电梯所在层数数组
        for i in range(1, 6):
            self.isUp[i] = False
            self.isDown[i] = False
            self.last_isUp[i] = False
            self.last_isDown[i] = False
            self.location[i] = 1
        self.upfloor = [[0] * 21 for i in range(6)]  # 记录某电梯将处理但未处理的楼层上行请求
        self.downfloor = [[0] * 21 for i in range(6)]  # 记录某电梯将处理但未处理的楼层下行请求
        self.upSequence = [[] for i in range(6)]  # 电梯上行序列数组
        self.downSequence = [[] for i in range(6)]  # 电梯下行序列数组

        for i in range(1, 20):  # 上行按钮与监听函数绑定
            self.ui.up_btn[i].clicked.connect(partial(self.upbutton_listen, i))
        for i in range(2, 21):  # 下行按钮与监听函数绑定
            self.ui.down_btn[i].clicked.connect(partial(self.downbutton_listen, i))
        for i in range(1, 6):
            for j in range(1, 21):  # 数字按钮与监听函数绑定
                self.ui.number_btn[i][j].clicked.connect(partial(self.numberbtn_listen, i, j))
        for i in range(1, 6):  # 加载线程
            self.thread(i)

    # 监听上行按钮
    def upbutton_listen(self, btn_number):
        self.ui.up_btn[btn_number].setStyleSheet("QPushButton{border-image: url(icon/up_pressed.png)}")
        upbtn_distance = [40, 40, 40, 40, 40, 40]  # 记录某楼层发出上行请求时,五部电梯兼顾处理自己的任务到达该楼层所要走的距离，初始化为40
        requestIsUp = {}  # 请求是否在电梯上方（包括本层）
        for i in range(1, 6):
            requestIsUp[i] = False
            if (btn_number - self.location[i]) >= 0:
                requestIsUp[i] = True
        for i in range(1, 6):
            if self.isUp[i] == True and self.isDown[i] == False:  # 上行状态
                if requestIsUp[i]:  # 请求在上方或本层
                    upbtn_distance[i] = abs(btn_number - self.location[i])  # 当前位置距请求位置距离
                else:  # 请求在下方
                    upbtn_distance[i] = abs(self.location[i] - self.upSequence[i][len(self.upSequence[i]) - 1]) \
                                        + abs(
                        btn_number - self.upSequence[i][len(self.upSequence[i]) - 1])  # 当前位置距终点距离 + 终点距请求位置距离
            elif self.isUp[i] == False and self.isDown[i] == False:  # 静止状态
                upbtn_distance[i] = abs(btn_number - self.location[i])  # 当前位置距请求位置距离
            elif self.isUp[i] == False and self.isDown[i] == True:  # 下行状态
                upbtn_distance[i] = abs(self.location[i] - self.downSequence[i][len(self.downSequence[i]) - 1]) \
                                    + abs(
                    btn_number - self.downSequence[i][len(self.downSequence[i]) - 1])  # 当前位置距终点距离 + 终点距请求位置距离
        elevator_number = upbtn_distance.index(min(upbtn_distance))  # 记录距离最短的电梯的序号
        if self.isUp[elevator_number] == True and self.isDown[elevator_number] == False:  # 上行状态
            if requestIsUp[elevator_number]:  # 请求在上方或本层
                self.upSequence[elevator_number].append(btn_number)  # 加入上行序列
                self.upSequence[elevator_number] = list(set(self.upSequence[elevator_number]))
                self.upSequence[elevator_number].sort()
            else:  # 请求在下方
                self.upfloor[elevator_number][btn_number] = 1  # 记录elevator_number电梯将处理但未处理的楼层上行请求
        elif self.isUp[elevator_number] == False and self.isDown[elevator_number] == False:  # 静止状态
            if requestIsUp[elevator_number]:  # 请求在上方或本层
                self.upSequence[elevator_number].append(btn_number)  # 加入上行序列
                self.upSequence[elevator_number] = list(set(self.upSequence[elevator_number]))
                self.upSequence[elevator_number].sort()
            else:  # 请求在下方
                self.downSequence[elevator_number] = list(set(self.downSequence[elevator_number]))
                self.downSequence[elevator_number].sort()
                self.downSequence[elevator_number].reverse()
                self.upfloor[elevator_number][btn_number] = 1  # 记录elevator_number电梯将处理但未处理的楼层上行请求
        elif self.isUp[elevator_number] == False and self.isDown[elevator_number] == True:  # 下行状态
            self.upfloor[elevator_number][btn_number] = 1  # 记录elevator_number电梯将处理但未处理的楼层上行请求

    # 监听下行按钮
    def downbutton_listen(self, btn_number):
        self.ui.down_btn[btn_number].setStyleSheet("QPushButton{border-image: url(icon/down_pressed.png)}")
        downbtn_distance = [40, 40, 40, 40, 40, 40]  # 记录某楼层发出下行请求时,五部电梯兼顾处理自己的任务到达该楼层所要走的距离,初始化为40
        requestIsDown = {}  # 请求是否在电梯下方（包括本层）
        for i in range(1, 6):
            requestIsDown[i] = False
            if (btn_number - self.location[i]) <= 0:
                requestIsDown[i] = True
        for i in range(1, 6):
            if self.isUp[i] == False and self.isDown[i] == True:  # 下行状态
                if requestIsDown[i]:  # 请求在下方或本层
                    downbtn_distance[i] = abs(self.location[i] - btn_number)  # 当前位置距请求位置距离
                else:  # 请求在下方
                    downbtn_distance[i] = abs(
                        self.location[i] - self.downSequence[i][len(self.downSequence[i]) - 1]) \
                                          + abs(btn_number - self.downSequence[i][
                        len(self.downSequence[i]) - 1])  # 当前位置距终点距离 + 终点距请求位置距离
            elif self.isUp[i] == False and self.isDown[i] == False:  # 静止状态
                downbtn_distance[i] = abs(self.location[i] - btn_number)  # 当前位置距请求位置距离
            elif self.isUp[i] == True and self.isDown[i] == False:  # 上行状态
                downbtn_distance[i] = abs(self.location[i] - self.upSequence[i][len(self.upSequence[i]) - 1]) \
                                      + abs(
                    btn_number - self.upSequence[i][len(self.upSequence[i]) - 1])  # 当前位置距终点距离 + 终点距请求位置距离
        elevator_number = downbtn_distance.index(min(downbtn_distance))  # 记录距离最短的电梯的序号
        if self.isUp[elevator_number] == False and self.isDown[elevator_number] == True:  # 下行状态
            if requestIsDown[elevator_number]:  # 请求在下方或本层
                self.downSequence[elevator_number].append(btn_number)  # 加入下行序列
                self.downSequence[elevator_number] = list(set(self.downSequence[elevator_number]))
                self.downSequence[elevator_number].sort()
                self.downSequence[elevator_number].reverse()
            else:  # 请求在上方
                self.downfloor[elevator_number][btn_number] = 1  # 记录elevator_number电梯将处理但未处理的楼层下行请求
        elif self.isUp[elevator_number] == False and self.isDown[elevator_number] == False:  # 静止状态
            if requestIsDown[elevator_number]:  # 请求在下方或本层
                self.downSequence[elevator_number].append(btn_number)
                self.downSequence[elevator_number] = list(set(self.downSequence[elevator_number]))
                self.downSequence[elevator_number].sort()
                self.downSequence[elevator_number].reverse()
            else:  # 请求在上方
                self.upSequence[elevator_number].append(btn_number)  # 加入上行序列
                self.upSequence[elevator_number] = list(set(self.upSequence[elevator_number]))
                self.upSequence[elevator_number].sort()
                self.downfloor[elevator_number][btn_number] = 1  # 记录elevator_number电梯将处理但未处理的楼层下行请求
        elif self.isUp[elevator_number] == True and self.isDown[elevator_number] == False:  # 上行状态
            self.downfloor[elevator_number][btn_number] = 1  # 记录elevator_number电梯将处理但未处理的楼层下行请求

    # 监听电梯楼层数字按钮，elevator_number:电梯序号，btn_number:按钮楼层号
    def numberbtn_listen(self, elevator_number, btn_number):
        if self.isUp[elevator_number] == False and self.isDown[elevator_number] == False:  # 电梯elevator_number处于静止状态
            if self.location[elevator_number] > btn_number:  # 电梯elevator_number当前位置在请求楼层之上
                self.ui.number_btn[elevator_number][btn_number].setStyleSheet(
                    "QPushButton{border-image: url(icon/" + str(btn_number) + "_pressed.png)}")
                self.downSequence[elevator_number].append(btn_number)  # 将请求加入电梯elevator_number的下行序列
                self.downSequence[elevator_number] = list(set(self.downSequence[elevator_number]))
                self.downSequence[elevator_number].sort()
                self.downSequence[elevator_number].reverse()
            if self.location[elevator_number] < btn_number:  # 电梯elevator_number当前位置在请求楼层之下
                self.ui.number_btn[elevator_number][btn_number].setStyleSheet(
                    "QPushButton{border-image: url(icon/" + str(btn_number) + "_pressed.png)}")
                self.upSequence[elevator_number].append(btn_number)  # 将请求加入电梯elevator_number的上行序列
                self.upSequence[elevator_number] = list(set(self.upSequence[elevator_number]))
                self.upSequence[elevator_number].sort()
        elif self.isUp[elevator_number] == True and self.isDown[elevator_number] == False:  # 电梯elevator_number处于上行状态
            if self.location[elevator_number] < btn_number:  # 电梯elevator_number当前位置在请求楼层之下，之上时不处理
                self.ui.number_btn[elevator_number][btn_number].setStyleSheet(
                    "QPushButton{border-image: url(icon/" + str(btn_number) + "_pressed.png)}")
                self.upSequence[elevator_number].append(btn_number)  # 将请求加入电梯elevator_number的上行序列
                self.upSequence[elevator_number] = list(set(self.upSequence[elevator_number]))
                self.upSequence[elevator_number].sort()
        elif self.isUp[elevator_number] == False and self.isDown[elevator_number] == True:  # 电梯elevator_number处于下行状态
            if self.location[elevator_number] > btn_number:  # 电梯elevator_number当前位置在请求楼层之上，之下时不处理
                self.ui.number_btn[elevator_number][btn_number].setStyleSheet(
                    "QPushButton{border-image: url(icon/" + str(btn_number) + "_pressed.png)}")
                self.downSequence[elevator_number].append(btn_number)  # 将请求加入电梯elevator_number的下行序列
                self.downSequence[elevator_number] = list(set(self.downSequence[elevator_number]))
                self.downSequence[elevator_number].sort()
                self.downSequence[elevator_number].reverse()
        else:
            print("error")

    # 创建线程
    def thread(self, elevator_number):
        t = threading.Thread(target=partial(self.elevator_anim, elevator_number))
        t.setDaemon(True)
        t.start()

    # 加载上行序列动画
    def elevator_up_anim(self, elevator_number):
        while len(self.upSequence[elevator_number]):  # 如果上行序列非空
            self.isUp[elevator_number] = True  # 置电梯状态为上行状态
            # self.ui.isup_label[elevator_number].setPixmap(QtGui.QPixmap("icon/isup.png"))
            # self.ui.isdown_label[elevator_number].setPixmap(QtGui.QPixmap("icon/isnotdown.png"))
            upSequence_0 = self.upSequence[elevator_number][0]  # 记录当前上行序列的第一个任务
            j = abs(
                self.upSequence[elevator_number][0] - self.location[elevator_number])  # 当前位置与上行序列的第一个任务相差的层数
            i = 1
            while i <= j:
                if upSequence_0 == self.upSequence[elevator_number][0]:  # 上行序列第一个任务未更新
                    time.sleep(0.5)
                    self.location[elevator_number] = self.location[elevator_number] + 1  # 更新location[elevator_number]
                    self.ui.elevator_label[elevator_number].setGeometry(  # 更新电梯label
                        QtCore.QRect(elevator_number * 100 - 92.5, 902.5 - 40 * self.location[elevator_number], 35, 35))
                    self.ui.location_label[elevator_number].setText(str(self.location[elevator_number]))  # 更新楼层显示
                else:  # 上行序列第一个任务更新
                    j = abs(self.upSequence[elevator_number][0] - self.location[
                        elevator_number])  # 更新当前位置与上行序列的第一个任务相差的层数
                    upSequence_0 = self.upSequence[elevator_number][0]  # 更新当前上行序列的第一个任务的记录
                    i = 0  # 重置i，考虑到后面存在+1，将i置为0
                i = i + 1
            time.sleep(0.5)  # 电梯到达目的楼层，停顿
            if self.upSequence[elevator_number][0] < 20:  # 还原按钮样式
                self.ui.up_btn[self.upSequence[elevator_number][0]].setStyleSheet(self.ui.upbtn_style)
            self.ui.number_btn[elevator_number][self.upSequence[elevator_number][0]].setStyleSheet(
                "QPushButton{border-image: url(icon/" + str(self.upSequence[elevator_number][0]) + "_hover.png)}"
                "QPushButton:hover{border-image: url(icon/" + str(self.upSequence[elevator_number][0]) + ".png)}"
                "QPushButton:pressed{border-image: url(icon/" + str(self.upSequence[elevator_number][0]) +
                "_pressed.png)}"
            )
            del self.upSequence[elevator_number][0]  # 删除序列中已处理完的楼层
        self.last_isUp[elevator_number] = self.isUp[elevator_number]  # 上行序列处理完毕，记录本次状态
        self.isUp[elevator_number] = False  # 上行序列处理完毕，取消电梯上行状态
        # self.ui.isup_label[elevator_number].setPixmap(QtGui.QPixmap("icon/isnotup.png"))
        # self.ui.isdown_label[elevator_number].setPixmap(QtGui.QPixmap("icon/isnotdown.png"))

    # 加载下行序列动画
    def elevator_down_anim(self, elevator_number):
        while len(self.downSequence[elevator_number]):  # 如果下行序列非空
            self.isDown[elevator_number] = True  # 置电梯状态为下行状态
            # self.ui.isup_label[elevator_number].setPixmap(QtGui.QPixmap("icon/isnotup.png"))
            # self.ui.isdown_label[elevator_number].setPixmap(QtGui.QPixmap("icon/isdown.png"))
            downSequence_0 = self.downSequence[elevator_number][0]  # 记录当前下行序列的第一个任务
            j = abs(
                self.downSequence[elevator_number][0] - self.location[elevator_number])  # 当前位置与下行序列的第一个任务相差的层数
            i = 1
            while i <= j:
                if downSequence_0 == self.downSequence[elevator_number][0]:  # 下行序列第一个任务未更新
                    time.sleep(0.5)
                    self.location[elevator_number] = self.location[elevator_number] - 1
                    self.ui.elevator_label[elevator_number].setGeometry(
                        QtCore.QRect(elevator_number * 100 - 92.5, 902.5 - 40 * self.location[elevator_number], 35, 35))
                    self.ui.location_label[elevator_number].setText(str(self.location[elevator_number]))
                else:  # 下行序列第一个任务更新
                    j = abs(self.downSequence[elevator_number][0] - self.location[elevator_number])  # 更新当前位置与下行序列的第一个任务相差的层数
                    downSequence_0 = self.downSequence[elevator_number][0]  # 更新当前下行序列的第一个任务的记录
                    i = 0  # 重置i，考虑到后面存在+1，将i置为0
                i = i + 1
            time.sleep(0.5)  # 电梯到达目的楼层，停顿
            if self.downSequence[elevator_number][0] > 1:  # 还原按钮样式
                self.ui.down_btn[self.downSequence[elevator_number][0]].setStyleSheet(self.ui.downbtn_style)
            self.ui.number_btn[elevator_number][self.downSequence[elevator_number][0]].setStyleSheet(
                "QPushButton{border-image: url(icon/" + str(self.downSequence[elevator_number][0]) + "_hover.png)}"
                "QPushButton:hover{border-image: url(icon/" +
                str(self.downSequence[elevator_number][0]) + ".png)}"
                "QPushButton:pressed{border-image: url(icon/" +
                str(self.downSequence[elevator_number][0]) + "_pressed.png)}")
            del self.downSequence[elevator_number][0]  # 删除序列中已处理完的楼层
        self.last_isDown[elevator_number] = self.isDown[elevator_number]  # 下行序列处理完毕，记录本次状态
        self.isDown[elevator_number] = False  # 下行序列处理完毕，取消电梯下行状态
        # self.ui.isup_label[elevator_number].setPixmap(QtGui.QPixmap("icon/isnotup.png"))
        # self.ui.isdown_label[elevator_number].setPixmap(QtGui.QPixmap("icon/isnotdown.png"))

    # 执行完上行动作恢复静止后，处理执行动作时产生的但未处理的请求
    # 此时执行动作时产生的但未处理的下行请求可能在任意位置，但执行动作时产生的但未处理的上行请求只可能在下方
    def elevator_finish_up(self, elevator_number):
        i = 20
        while i >= 1:  # 倒序处理执行动作时产生的但未处理的下行请求
            if self.downfloor[elevator_number][i] == 1:
                if i > self.location[elevator_number]:  # 上方存在执行动作时产生的但未处理的下行请求
                    self.upSequence[elevator_number].append(i)  # 将最高楼层的下行请求加入上行序列,继续上行
                    self.upSequence[elevator_number] = list(set(self.upSequence[elevator_number]))
                    self.isUp[elevator_number] = True
                    # self.ui.isup_label[elevator_number].setPixmap(QtGui.QPixmap("icon/isup.png"))
                    # self.ui.isdown_label[elevator_number].setPixmap(QtGui.QPixmap("icon/isnotdown.png"))
                    break
                # 上方不存在执行动作时产生的但未处理的下行请求
                self.downfloor[elevator_number][i] = 0
                self.downSequence[elevator_number].append(i)  # 将记录的上方的上行请求加入上行序列，开始上行
                self.downSequence[elevator_number] = list(set(self.downSequence[elevator_number]))
                self.downSequence[elevator_number].sort()
                self.downSequence[elevator_number].reverse()
                self.isDown[elevator_number] = True
            i = i - 1
        # 不存在下行请求，处理执行动作时产生的但未处理的上行请求（该请求只可能在下方）
        if self.isDown[elevator_number] == False and self.isUp[elevator_number] == False:
            for i in range(1, 21):  # 正序处理
                if self.upfloor[elevator_number][i] == 1:
                    self.downSequence[elevator_number].append(i)  # 将最底楼层的下行请求加入下行序列,开始下行
                    self.downSequence[elevator_number] = list(set(self.downSequence[elevator_number]))
                    self.isDown[elevator_number] = True
                    break

    # 执行完下行动作恢复静止后，处理执行动作时产生的但未处理的请求
    # 此时执行动作时产生的但未处理的上行请求可能在任意位置，但执行动作时产生的但未处理的下行请求只可能在上方
    def elevator_finish_down(self, elevator_number):
        i = 1
        while i <= 20:  # 正序处理执行动作时产生的但未处理的上行请求
            if self.upfloor[elevator_number][i] == 1:
                if i < self.location[elevator_number]:  # 下方存在执行动作时产生的但未处理的上行请求
                    self.downSequence[elevator_number].append(i)  # 将最低楼层的上行请求加入下行序列,继续下行
                    self.downSequence[elevator_number] = list(set(self.downSequence[elevator_number]))
                    self.isDown[elevator_number] = True
                    break
                # 下方不存在执行动作时产生的但未处理的上行请求
                self.upfloor[elevator_number][i] = 0
                self.upSequence[elevator_number].append(i)  # 将记录的上方的上行请求加入上行序列，开始上行
                self.upSequence[elevator_number] = list(set(self.upSequence[elevator_number]))
                self.upSequence[elevator_number].sort()
                self.isUp[elevator_number] = True
            i = i + 1
        # 不存在上行请求，处理执行动作时产生的但未处理的下行请求（该请求只可能在上方）
        if self.isUp[elevator_number] == False and self.isDown[elevator_number] == False:
            i = 20  # 倒序处理
            while i >= 1:
                if self.downfloor[elevator_number][i] == 1:
                    self.upSequence[elevator_number].append(i)  # 将最高楼层的下行请求加入上行序列,开始上行
                    self.upSequence[elevator_number] = list(set(self.upSequence[elevator_number]))
                    self.isUp[elevator_number] = True
                    break
                i = i - 1

    # 每趟动画执行完后，对该趟动画执行时产生的未能执行的数据进行处理
    def finish_anim(self, elevator_number):
        if self.last_isUp[elevator_number] == False and self.last_isDown[elevator_number] == False:  # 电梯初始状态
            self.elevator_finish_down(elevator_number)  # 执行完下行动作恢复静止后，处理执行动作时产生的但未处理的请求
        elif self.last_isUp[elevator_number] == True and self.last_isDown[elevator_number] == False:  # 执行完上行动作后
            self.elevator_finish_up(elevator_number)  # 执行完上行动作恢复静止后，处理执行动作时产生的但未处理的请求
        elif self.last_isUp[elevator_number] == False and self.last_isDown[elevator_number] == True:  # 执行完下行动作后
            self.elevator_finish_down(elevator_number)  # 执行完下行动作恢复静止后，处理执行动作时产生的但未处理的请求

    # 加载电梯动画
    def elevator_anim(self, elevator_number):
        while 1:
            if self.isUp[elevator_number] == False and self.isDown[elevator_number] == False:  # 电梯处于静止状态
                self.elevator_up_anim(elevator_number)  # 加载上行序列动画
                self.finish_anim(elevator_number)
                self.elevator_down_anim(elevator_number)  # 加载下行序列动画
                self.finish_anim(elevator_number)
            elif self.isUp[elevator_number] == True and self.isDown[elevator_number] == False:  # 电梯处于上行状态
                self.elevator_up_anim(elevator_number)  # 加载上行序列动画
                self.finish_anim(elevator_number)
            elif self.isUp[elevator_number] == False and self.isDown[elevator_number] == True:  # 电梯处于下行状态
                self.elevator_down_anim(elevator_number)  # 加载下行序列动画
                self.finish_anim(elevator_number)