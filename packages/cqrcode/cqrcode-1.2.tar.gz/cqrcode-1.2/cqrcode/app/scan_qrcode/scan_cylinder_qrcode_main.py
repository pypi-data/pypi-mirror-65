# coding: utf-8
# !/usr/bin/python
"""
@File       :   scan_cylinder_qrcode_main.py
@Author     :   jiaming
@Modify Time:   2020/4/3 20:00
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   None
"""
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from cqrcode.static._static_data import dataPath


def return_start_point(figure=None):
    """

    :param figure:
    :return:
    """
    width, height = figure.size
    img_array = figure.load()
    x = y = -1
    for i in range(width//8):
        for j in range(height//8):
            # 白色
            if img_array[i, j] == (255, 255, 255):
                # 水平 x
                for k in range(i, width//8):
                    # print(k, j)
                    if img_array[k, j] != (255, 255, 255):
                        break
                else:
                    x = i
                # 垂直 y
                for k in range(j, height//8):
                    # print(i, k)
                    if img_array[i, k] != (255, 255, 255):
                        break
                else:
                    y = j
                if x != -1 and y != -1 and img_array[i+1, y+1] == (0, 0, 0):
                    # figure.putpixel((x, y), (255, 0, 0))
                    # figure.save(dataPath+'tmp.png')
                    return x, y


def return_box(figure_path=None):
    """

    :param figure:
    :return:
    """
    figure = Image.open(figure_path)
    figure = figure.convert('RGB')
    width, height = figure.size
    img_array = figure.load()
    print('图片尺寸：', width, height)
    # 返回图案的起始坐标
    x, y = return_start_point(figure)
    print('start point: ', x, y)
    boxlist = []

    # 检测图案的宽度
    count = 0
    for i in range(x+1, width):
        if img_array[i, y+1] == (0, 0, 0):
            count += 1
        else:
            break
    boxlist.append(count//5)

    # 检测图案的长度
    x1 = y1 = -1
    count = 0
    for j in range(y+1, height):
        if img_array[x+1, j] == (0, 0, 0):
            count += 1
        else:
            x1 = x
            y1 = j
            break
    boxlist.append(count//5)

    # 探究高度的一半处的尺寸（厚度）
    count = 0
    for i in range(1, width):
        if img_array[x1 + i, (y1-y)//2] == (0, 0, 0):
            count += 1
        else:
            break
    boxlist.append(count)
    prebox = int(round(sum(boxlist)/len(boxlist), 0))

    # 探测纵向线
    tmplistblack = []
    countblack = 0
    for j in range(y, height):
        # figure.putpixel((x+prebox//2, j), (255, 0, 0))
        if img_array[x+prebox//2, j] == (0, 0, 0):
            countblack += 1
        else:
            tmplistblack.append(countblack)
            countblack = 0

    # 探测纵向线 + 1
    countblack = 0
    for j in range(y, height):
        # figure.putpixel((x + prebox // 2 + 1, j), (255, 0, 0))
        if img_array[x + prebox // 2 + 1, j] == (0, 0, 0):
            countblack += 1
        else:
            tmplistblack.append(countblack)
            countblack = 0

    from collections import Counter
    word_counts = Counter(tmplistblack)
    # 出现频率最高的
    top_five = word_counts.most_common(5)
    print(top_five)
    for i in top_five:
        if i[0] != 0:
            boxlist.append(i[0])
            break

    print(boxlist)


def returnBitOrNot(figure=None, coordinate=None, rate=0.8, step=5):
    """

    :param figure:
    :param coordinate:
    :param rate:
    :param step:
    :return:
    """
    pass


def return_version(figure=None, coordinate=None, box=-1):
    """

    :param figure:
    :param coordinate:
    :param box:
    :return:
    """
    pass



def scan_qrcode(image_file=dataPath + 'target1.png'):
    """

    :param image_path:
    :return:
    """
    # 0, 读入图片

    image = cv2.imread(image_file)

    # 1，先将读入的摄像头frame转换成灰度图：

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_file = dataPath + 'gray.png'

    # 2，使用算子进行过滤：
    Laplacian = cv2.Laplacian(gray, cv2.CV_32F, ksize=3)

    # 3，将过滤得到的X方向像素值减去Y方向的像素值：

    # ...

    # 4，先缩放元素再取绝对值，最后转换格式为8bit型

    Laplacian_img = cv2.convertScaleAbs(Laplacian)
    laplacian_file = dataPath + 'laplacian.png'

    # 5，均值滤波取二值化：
    """
    blur
    参数解释：
    . InputArray src: 输入图像，可以是Mat类型，图像深度是CV_8U、CV_16U、CV_16S、CV_32F以及CV_64F其中的某一个。
    . OutputArray dst: 输出图像，深度和类型与输入图像一致
    . Size ksize: 滤波模板kernel的尺寸，一般使用Size(w, h)来指定，如Size(3,3)
    . Point anchor=Point(-1, -1): 字面意思是锚点，也就是处理的像素位于kernel的什么位置，默认值为(-1, -1)即位于kernel中心点，如果没有特殊需要则不需要更改
    . int borderType=BORDER_DEFAULT: 用于推断图像外部像素的某种边界模式，有默认值BORDER_DEFAULT
    """
    blurred = cv2.blur(Laplacian_img, (3, 3))
    """
    threshold
    threshold是设定的阈值
    maxval是当灰度值大于（或小于）阈值时将该灰度值赋成的值
    type规定的是当前二值化的方式
    """
    (_, thresh) = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY)
    thresh_file = dataPath + 'thresh.png'

    # 6，腐蚀和膨胀的函数：

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    erode_dilate_file = dataPath + 'erode_dilate.png'

    # 7，找到边界findContours函数

    cnts, hierarchy = cv2.findContours(closed.copy(),
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
    # 8，计算出包围目标的最小矩形区域：
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    rect = cv2.minAreaRect(c)  # minAreaRect就是求出在点集下的最小面积矩形 return:
    # (中心点坐标，长宽，旋转角度[-90,0))，当矩形水平或竖直时均返回-90
    width, height = rect[1]
    print('矩形：', rect)
    box = np.int0(cv2.boxPoints(rect))  # 获取最小外接矩形的4个顶点坐标
    print('最小外接矩形4个顶点坐标:', box, type(box))
    cv2.drawContours(image, [box], 0, (255, 0, 0), 3)  # 绘制矩形区域
    drawContours_file = dataPath + 'drawContours.png'

    # 9, 识别二维码的区域，透视变换:

    new_width = int(width)
    new_height = int(height)
    pts1 = np.float32([box])
    pts2 = np.float32(
        [[0, new_height], [0, 0], [new_width, 0], [new_width, new_height]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warpPerspective = cv2.warpPerspective(gray, M, (new_width, new_height))
    warpPerspective_file = dataPath + 'warpPerspective_file.png'
    (_, thresh_warpPerspective) = cv2.threshold(
        warpPerspective, 0, 255, cv2.THRESH_OTSU)
    thresh_warpPerspective_file = dataPath + 'thresh_warpPerspective.png'

    # 10, 保存结果

    # 保存灰度图
    cv2.imwrite(
        gray_file, gray
    )
    # 保存拉普拉斯算子处理后图片
    cv2.imwrite(
        laplacian_file, Laplacian_img
    )
    # 保存二值化后图片
    cv2.imwrite(
        thresh_file, thresh
    )
    # 保存绘制轮廓后的图片
    cv2.imwrite(
        drawContours_file, image
    )
    # 保存腐蚀膨胀的图像
    cv2.imwrite(
        erode_dilate_file, closed
    )
    # 保存透视变换后的图片
    cv2.imwrite(
        warpPerspective_file, warpPerspective
    )
    # 保存提取后的二维码的二值化图
    cv2.imwrite(
        thresh_warpPerspective_file, thresh_warpPerspective
    )

    # 11, 显示结果

    filePath = [
        image_file,
        gray_file,
        laplacian_file,
        thresh_file,
        erode_dilate_file,
        drawContours_file,
        warpPerspective_file,
        thresh_warpPerspective_file,
    ]
    for i in range(len(filePath)):
        plt.title(str(i))
        plt.subplot(3, 3, i + 1)
        img = cv2.imread(filePath[i], 3)
        plt.xticks([])
        # plt.yticks([])
        plt.imshow(img)
    plt.title(str(len(filePath)))
    file = dataPath + "procession.png"
    plt.savefig(file, dpi=300, bbox_inchs='tight')
    plt.show()

    # 返回元码像素尺寸


    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # scan_qrcode()
    return_box(figure_path=dataPath+'thresh_warpPerspective.png')
