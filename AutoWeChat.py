"""
Des 主程序类
@Author thetheOrange
Time 2023/12/16
"""
import sys
from threading import Thread

from PyQt5.QtWidgets import QWidget, QLineEdit, QMessageBox, QApplication

from autoCore import AutoCore
from globalSignals import global_signal
from handleConfig import read_config, modify_config
from windows.settingWindow import settingWindow


# 子线程，负责发送信息
class AutoSend(Thread):
    def __init__(self, name, loop_flag, interval, text_box):
        super().__init__()
        self.start_flag = True
        self.auto_core = AutoCore()
        self.auto_core.user_name = name
        self.auto_core.loop_flag = loop_flag
        self.auto_core.loop_interval = interval
        self.auto_core.text_box = text_box

    def run(self):
        self.auto_core.start()

    def stop(self):
        self.auto_core.stop()


class AutoWeChat(QWidget):

    def __init__(self):
        super().__init__()
        # 读取配置文件
        self.__config = read_config()
        # 消息列表
        self.__text_box = self.__config.get("text_box")
        # 循环间隔
        self.__interval = self.__config.get("interval")

        self.set_w = settingWindow()
        # 展示历史信息
        self.set_w.show_msg.setPlainText(f"{self.__text_box}")
        self.set_w.interval_spin.setValue(self.__interval)
        # 循环标志
        self.__loop_flag = True

        # 处理设置窗口的信号
        global_signal.Operation.connect(self.__handle_signal)
        # 处理循环信号
        global_signal.Isloop.connect(self.__loop)
        # 处理设置循环间隔
        global_signal.Interval.connect(self.__set_interval)

    # 处理信号
    def __handle_signal(self, value):
        if value == "Start":
            self.__start()
        if value == "Stop":
            self.__stop()
        if value == "Add/Delete":
            self.__add_msg()
        if value == "Clear":
            self.__clear_msg()

    # 程序开始
    def __start(self):
        try:
            # 获取用户名输入控件
            user_name = self.set_w.findChild(QLineEdit, "userEdit").text()
            user_name = str(user_name)
            if user_name != "" and len(self.__text_box) > 0:
                # 消息列表
                self.__text_box = self.__config.get("text_box")
                # 循环间隔
                self.__interval = self.__config.get("interval")
                self.auto_send_t = AutoSend(name=user_name, loop_flag=self.__loop_flag,
                                            interval=self.__interval, text_box=self.__text_box)
                self.auto_send_t.start()
                self.set_w.setWindowTitle("Sending...")
            else:
                msg_box = QMessageBox(QMessageBox.Critical, '错误', '请检查用户名和文本列表是否为空!')
                msg_box.exec_()
        except Exception as e:
            print(e)

    # 结束发送
    def __stop(self):
        self.set_w.setWindowTitle("AutoWeChat-Setting")
        self.auto_send_t.stop()

    # 加入循环
    def __loop(self, value):
        if value:
            self.__loop_flag = True
        else:
            self.__loop_flag = False

    # 设置循环间隔
    @staticmethod
    def __set_interval(value):
        modify_config(key="interval", value=value)

    # 加入/删除消息文本
    def __add_msg(self):
        try:
            # 获取消息文本输入控件
            text_input = self.set_w.findChild(QLineEdit, "msgEdit").text()
            text_input = str(text_input)
            if text_input != "":
                if text_input in self.__text_box:
                    self.__text_box.remove(text_input)
                    modify_config(key="text_box", value=self.__text_box)
                    self.set_w.show_msg.setPlainText(f"{self.__text_box} ")
                else:
                    self.__text_box.append(text_input)
                    modify_config(key="text_box", value=self.__text_box)
                    self.set_w.show_msg.setPlainText(f"{self.__text_box} ")
            elif text_input == "":
                msg_box = QMessageBox(QMessageBox.Critical, '错误', '消息不能为空!')
                msg_box.exec_()
        except Exception as e:
            print(e)

    # 清空消息列表
    def __clear_msg(self):
        self.__text_box = []
        modify_config(key="text_box", value=self.__text_box)
        self.set_w.show_msg.setPlainText(str(self.__text_box))
