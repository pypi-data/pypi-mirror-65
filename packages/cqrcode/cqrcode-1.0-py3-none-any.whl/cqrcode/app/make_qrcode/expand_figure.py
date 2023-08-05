# coding: utf-8 
# !/usr/bin/python
"""
@File       :   expand_figure.py
@Author     :   jiaming
@Modify Time:   2020/4/3 14:59    
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   None
"""
import math
from PIL import Image
from cqrcode.static._static_data import dataPath


def expand_fig(multiplying_power=0.20, version=-1, filePath=''):
    """
    水平拉伸图片
    1 mm = 10 像素
    1 像素 = 0.1 mm
    :param multiplying_power:
    :return:
    """

    print('进行二维码拓展 %s...' % str(multiplying_power))
    INPUT_IMAGE = Image.open(filePath)
    w, h = INPUT_IMAGE.size

    width = w
    L = 350  # 固定值（mm）
    R = 0.1 * width / multiplying_power  # 圆柱体半径（mm）
    x = [0.1 * i for i in range(0, width // 2, 1)]  # （mm）
    y = []

    for i in x:
        # 将移动的单位换算为像素
        y.append((math.asin(((R + L) / R) * math.sin(math.atan(i / L)))
                  - math.atan(i / L)) * R * 10 - i * 10)
    y.reverse()
    # 读入空白图片
    OUT_IMAGE = INPUT_IMAGE.resize((2 * round(y[0]) + width, h), Image.ANTIALIAS)
    filePath = dataPath + '%s 扩展图片.png' % version
    OUT_IMAGE.save(filePath)
    print('扩展二维码成功 %s %s.' % (OUT_IMAGE, filePath))
    return filePath


if __name__ == "__main__":
    expand_fig(multiplying_power=1.5, version=1, filePath=dataPath+'1.png')