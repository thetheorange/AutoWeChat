"""
Des 微信自动化发送信息的核心
@Author thetheOrange
Time 2023/12/16
"""
import random
import time

import win32api
import win32clipboard
import win32con
import win32gui


class AutoCore:

    def __init__(self):
        # 用户名
        self.user_name = None
        # 文本列表
        self.text_box = []
        # 循环标志
        self.loop_flag = False
        # 循环时间间隔
        self.loop_interval = 1
        # 开启标志
        self.start_flag = True

    # 获取目标窗口
    def get_win(self):
        try:
            # 获取窗口句柄
            win = win32gui.FindWindow("ChatWnd", self.user_name)
            # 将窗口置于前台，便于控制
            win32gui.SetForegroundWindow(win)
            return True
        except Exception as e:
            print(f"找不到目标窗口, 请重试, 错误:{e}")
            return False

    # 将文本加入剪切版
    @staticmethod
    def add_msg(msg):
        try:
            # 打开剪切板
            win32clipboard.OpenClipboard()
            # 初始化剪切版
            win32clipboard.EmptyClipboard()
            # 添加文本输出
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, msg)
            print(f"已将{msg}添加到剪切版中")
        except Exception as e:
            print(e)
        finally:
            # 关闭剪切版
            win32clipboard.CloseClipboard()

    # 模拟粘贴操作
    @staticmethod
    def paste_op():
        # 按下ctrl+v
        win32api.keybd_event(17, 0, 0, 0)
        win32api.keybd_event(86, 0, 0, 0)
        # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)

    # 模拟发送操作
    @staticmethod
    def send_op():
        # 按下alt+s
        win32api.keybd_event(18, 0, 0, 0)
        win32api.keybd_event(83, 0, 0, 0)
        # 释放按键
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)

    # 随机文本生成
    def generate_text(self):
        text = random.choice(self.text_box)
        return text

    # 开启项目
    def start(self):
        while self.get_win() and self.start_flag:
            if self.loop_flag:
                text = self.generate_text()
                self.add_msg(msg=text)
                self.paste_op()
                self.send_op()
                time.sleep(random.uniform(0, self.loop_interval))
            else:
                text = self.generate_text()
                self.add_msg(msg=text)
                self.paste_op()
                self.send_op()
                break

    # 关闭项目
    def stop(self):
        self.start_flag = False


# 测试代码
if __name__ == "__main__":
    app = AutoCore()
    app.user_name = "刘子千"
    app.text_box.append("测试")
    app.loop_flag = True
    app.start()
    time.sleep(2)
    app.stop()
