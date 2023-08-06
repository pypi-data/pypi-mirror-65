# coding: utf-8
# !/usr/bin/python
"""
@File       :   QRcode.py
@Author     :   jiaming
@Modify Time:   2020/1/13 19:55
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   生成传统二维码
                解析传统二维码
"""
import qrcode
from PIL import Image
from pyzbar import pyzbar
from cqrcode.static._static_data import dataPath, BOUNDARY, BOX


def create_QRcode(data=''):
    """
    创建二维码, 并保存到 static/ 下
    :return: 生成的二维码路径
    """
    print('生成传统二维码...')
    filePath = dataPath + "传统二维码" + ".png"

    # 向二维码中填充数据
    """
    version：值为1~40的整数，控制二维码的大小（最小值是1，是个12×12的矩阵）。 如果想让程序自动确定，将值设置为 None 并使用 fit 参数即可。
    error_correction：控制二维码的错误纠正功能。可取值下列4个常量。
        ERROR_CORRECT_L：大约7%或更少的错误能被纠正。
        ERROR_CORRECT_M（默认）：大约15%或更少的错误能被纠正。
        ROR_CORRECT_H：大约30%或更少的错误能被纠正。
        ERROR_CORRECT_Q:至多能够矫正25%的错误。
    box_size：控制二维码中每个小格子包含的像素数。
    border：控制边框（二维码与图片边界的距离）包含的格子数（默认为4，是相关标准规定的最小值）。
    """
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=BOX,
        border=BOUNDARY,
    )  # 设置图片格式
    qr.add_data(data)
    qr.make(fit=True)
    # 生成二维码
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(filePath, dpi=(254.0, 254.0))
    print('保存路径：', filePath)
    return filePath


def decode_QRcode(filePath=''):
    """
    :param filePath: 待识别二维码路径
    :return: 打印出识别的结果
    """
    decode_data = pyzbar.decode(Image.open(filePath), symbols=[
        pyzbar.ZBarSymbol.QRCODE])[0].data.decode('utf-8')
    return decode_data


if __name__ == "__main__":
    create_QRcode('xxx')
