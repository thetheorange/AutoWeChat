# 测试代码
import sys

from PyQt5.QtWidgets import QApplication

from AutoWeChat import AutoWeChat

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoWeChat()
    window.set_w.show()
    app.exec()
