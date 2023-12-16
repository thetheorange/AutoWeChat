"""
Des 设置窗口初始化，绑定控件信号
@Author thetheOrange
Time 2023/12/16
"""
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QRadioButton, QDoubleSpinBox, QPlainTextEdit
from PyQt5.uic import loadUi

from globalSignals import global_signal

icon_path = "ui/chat.ico"


class settingWindow(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/setting_window.ui", self)
        # 设置标题、图标
        self.setWindowTitle("AutoWeChat-Setting")
        self.setWindowIcon(QIcon(icon_path))

        # 获取判断循环按钮并设置默认选中
        self.loop_button = self.findChild(QRadioButton, "loopButton")
        self.loop_button.setChecked(True)
        # 获取循环间隔控件并初始化范围
        self.interval_spin = self.findChild(QDoubleSpinBox, "doubleSpinBox")
        self.interval_spin.setRange(1.0, 10.0)
        self.interval_spin.setSingleStep(0.5)
        # 获取消息展示界面并设置为只读
        self.show_msg = self.findChild(QPlainTextEdit, "msgShow")
        self.show_msg.setReadOnly(True)

        self.init_ui()

    # 初始化各项控件，绑定信号
    def init_ui(self):
        # 寻找窗口按钮
        self.findChild(QPushButton, "searchButton").clicked.connect(lambda: global_signal.Operation.emit("Start"))
        # 停止按钮
        self.findChild(QPushButton, "stopButton").clicked.connect(lambda: global_signal.Operation.emit("Stop"))
        # 循环间隔
        self.interval_spin.valueChanged.connect(lambda value: global_signal.Interval.emit(value))
        # 判断循换按钮
        self.loop_button.toggled.connect(lambda: global_signal.Isloop.emit(self.loop_button.isChecked()))
        # 加入或删除文本按钮
        self.findChild(QPushButton, "addDeleteButton").clicked.connect(lambda: global_signal.Operation.emit("Add/Delete"))
        # 清空文本按钮
        self.findChild(QPushButton, "clearButton").clicked.connect(lambda: global_signal.Operation.emit("Clear"))


# 测试代码
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = settingWindow()
    window.show()
    app.exec()
