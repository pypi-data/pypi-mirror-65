# coding: utf-8
# !/usr/bin/python
"""
@File       :   Welcome.py
@Author     :   jiaming
@Modify Time:   2020/1/16 14:06
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   主界面，各主要功能入口
"""
import tkinter as tk

# 扫描功能入口
from cqrcode.app.scan_qrcode.scan_cylinder_qrcode_main import scan_qrcode
# 生成柱形二维码入口
from cqrcode.app.make_qrcode.create_cylinder_qrcode_main import create_cqrcode
# 生成普通二维码入口
from cqrcode.app.make_qrcode.QRcode import create_QRcode
# 呈现结果入口
from cqrcode.view.GUI_view import window
from cqrcode.static._static_data import dataPath

# 滑动条值
scaleValue = None
# 存储输入的字符串
input_txt = ''


def hello():
    """
    打开初始界面
    主界面，各主要功能入口：
    0.输入文本内容
    1.扫描二维码
    2.生成扩展后的柱形二维码
    3.设置比例
    :return:
    """
    root = tk.Tk()
    # root.iconbitmap(dataPath + r'/icon/welcome.ico')
    root.title("Welcome")
    root.geometry('300x230+504+248')
    root.resizable(False, False)
    # root.resizable(True, True)

    # 放置图片
    def putImage():
        """
        :return:
        """
        photoLabel = tk.Label()
        path = dataPath + '_blank.png'
        bm = tk.PhotoImage(file=path)
        photoLabel.x = bm
        photoLabel['image'] = bm
        photoLabel.pack()
    putImage()

    def click_btn_scan_figure_cmd(btn=None):
        """

        :param btn:
        :return:
        """
        # 调用摄像头，准备拍照
        # TODO：调用摄像头入口
        print('仅供树莓派...')
        pass
    scanBtn = tk.Button(root, text='Scan figure', bd=5, height=1,
                        relief=tk.GROOVE, width=27, activeforeground="#ffffff")
    scanBtn.config(command=lambda: click_btn_scan_figure_cmd(scanBtn))
    scanBtn.pack()

    # 键入文本按钮
    def click_btn_type_cmd(btn=None):
        """
        :param btn:
        :return:
        """
        global input_txt
        # Win
        input_txt = input('input sentences: ')
        print('well done!')
        print('_input.txt: ', input_txt)
        # Linux
        # print('loading _input.txt...\n')
        # p = os.system('nano /tmp/_input.txt')
        # with open('/tmp/_input.txt', 'r') as f:
        #     # print('input sentences: ', f.read())
        #     input_txt = f.read()
        # print('well done!')
        # print('_input.txt: ', input_txt)

    editBtn = tk.Button(root, text='Type the text', bd=5, height=1,
                        relief=tk.GROOVE, width=27, activeforeground="#ffffff")
    editBtn.config(command=lambda: click_btn_type_cmd(editBtn))
    editBtn.pack()

    def scale_command(ev=None):
        """
        :return:
        """
        global scaleValue
        scaleValue = horizontalScale.get()

    # 滑动条
    horizontalScale = tk.Scale(root, from_=0, to=1.5, tickinterval=0.5,
                               resolution=0.01, length=200,
                               orient=tk.HORIZONTAL, command=scale_command)
    horizontalScale.set(0.2)  # 不延展
    horizontalScale.pack()

    # label
    tk.Label(
        root,
        text='Length / Radius(*0.1mm)',
        font='Helvetica -11').pack()

    def output_cmd(btn=None):
        """

        :return:
        """
        print("二维码边长 / 圆柱体半径： ", float(horizontalScale.get()))
        # 生成传统二维码
        original_qrcode_path = create_QRcode(input_txt)
        # 生成延展的柱体二维码
        expand_cqrcode_path = create_cqrcode(data=input_txt, version=None,
                                       rate=float(horizontalScale.get()))
        window(original_qrcode_path=original_qrcode_path, cqrcode_path=expand_cqrcode_path)

    # 导出按钮
    createCodeBtn = tk.Button(root, width=15, height=2, text='outPut',
                              font='Helvetica -18', fg='red',
                              activebackground='#f0f0f0', relief=tk.GROOVE)
    createCodeBtn.config(command=output_cmd)
    createCodeBtn.pack()
    root.mainloop()


if __name__ == "__main__":
    hello()
