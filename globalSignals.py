"""
Des 各项控件的全局信号
@Author thetheOrange
Time 2023/12/16
"""
from PyQt5.QtCore import QObject, pyqtSignal


class GlobalSignal(QObject):
    # 操作类型信号
    Operation = pyqtSignal(str)
    # 循环间隔信号
    Interval = pyqtSignal(float)
    # 判断循环信号
    Isloop = pyqtSignal(bool)


global_signal = GlobalSignal()
