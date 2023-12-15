import random
import time

import win32api
import win32clipboard
import win32con
import win32gui


# 获取目标窗口
def get_win(name):
    try:
        # 获取窗口句柄
        win = win32gui.FindWindow("ChatWnd", name)
        # 将窗口置于前台，便于控制
        win32gui.SetForegroundWindow(win)
        return True
    except Exception as e:
        print(f"找不到目标窗口, 请重试, 错误:{e}")
        return False


# 将文本加入剪切版
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
def paste_op():
    # 按下ctrl+v
    win32api.keybd_event(17, 0, 0, 0)
    win32api.keybd_event(86, 0, 0, 0)
    # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)


# 模拟发送操作
def send_op():
    # 按下alt+s
    win32api.keybd_event(18, 0, 0, 0)
    win32api.keybd_event(83, 0, 0, 0)
    # 释放按键
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)


# 随机文本生成
def generate_text():
    text_box = ["[炸弹]"]
    text = random.choice(text_box)
    return text


def main(des_name):
    # 获取目标窗口
    while get_win(name=des_name):
        text = generate_text()
        add_msg(msg=text)
        paste_op()
        send_op()
        time.sleep(random.uniform(0.5, 0.8))


if __name__ == "__main__":
    name = "刘子千"
    main(des_name=name)
