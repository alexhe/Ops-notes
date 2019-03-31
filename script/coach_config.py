import time
import os


def load_file():
    """ 加载需要刷入的配置 """
    filePath = crt.Dialog.FileOpenDialog("请选择配置文档的位置", "Open", "coach.txt", "Log Files (*.txt)|*.txt")
    file = open(filePath)
    return file


def send_config(file):
    """ 刷如配置 """
    for read_line in file:
        crt.Screen.WaitForStrings([">","#"])
        index = crt.Screen.MatchIndex
        if index:
            time.sleep(0.1)
            crt.Screen.Send(read_line.strip('\r\n') + chr(13))


def main():
    file = load_file()
    send_config(file)
    file.close()


main()
