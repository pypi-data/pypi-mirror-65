# coding: utf-8 
# !/usr/bin/python
"""
@File       :   prepare_moudle.py
@Author     :   jiaming
@Modify Time:   2020/4/2 20:56    
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   None
"""
from PIL import Image
from cqrcode.static._static_data import height_length_table, BOX, BOUNDARY, dataPath


def put_pixel(figure=None, coordinate=()):
    """

    :param coordinate:
    :return:
    """
    for i in range(BOX):
        for j in range(BOX):
            figure.putpixel((coordinate[0] * BOX + i, coordinate[1]*BOX +
                             j), (0, 0, 0))


def moudle_figure(version=-1):
    """
    准备柱面二维码的模板
    :param version:
    :return:
    """
    height, length = height_length_table[version]
    figure = Image.new('RGB', (height*BOX+BOUNDARY*BOX*2,
                            length*BOX+BOUNDARY*BOX*2),
                      (255, 255, 255))
    print('%s 白板生成成功！' % version)
    # 绘制模板
    for i in range(BOUNDARY, BOUNDARY+5, 1):
        put_pixel(figure, (i, BOUNDARY))
    for j in range(BOUNDARY+1, BOUNDARY+4, 1):
        put_pixel(figure, (BOUNDARY, j))
        put_pixel(figure, (BOUNDARY+4, j))
    for i in range(BOUNDARY, BOUNDARY + 5, 1):
        put_pixel(figure, (i, BOUNDARY+4))
    put_pixel(
        figure,
        (BOUNDARY+2, BOUNDARY+2)
    )
    for i in range(BOUNDARY, height, 2):
        put_pixel(figure, (i, BOUNDARY))
    for j in range(BOUNDARY, length, 2):
        put_pixel(figure, (BOUNDARY, j))
    print('%s 模板生成成功！' % version)
    moudle_filePath = dataPath + '%s 模板.png' % version
    figure.save(moudle_filePath)
    return figure


def draw_mask(figure=None, version=-1):
    """
    绘制掩码
    :param figure: 模板
    :return:
    """
    height, length = height_length_table[version]
    # 绘制上下
    for i in range(height+2*BOUNDARY):
        for j in range(BOUNDARY):
            put_pixel(figure, (i, j))
            put_pixel(figure, (i, j+1))
    for i in range(height+2*BOUNDARY):
        for j in range(length+BOUNDARY, length+2*BOUNDARY):
            put_pixel(figure, (i, j))
    # 绘制两边
    for j in range(0, 2*BOUNDARY+length, 1):
        for i in range(BOUNDARY):
            put_pixel(figure, (i, j))
            put_pixel(figure, (i+1, j))
        for i in range(BOUNDARY):
            put_pixel(figure, (i + height + BOUNDARY, j))
    for i in range(BOUNDARY, BOUNDARY+6):
        for j in range(BOUNDARY, BOUNDARY+6, 1):
            put_pixel(figure, (i, j))
    print('%s 掩码生成成功！' % version)
    mask_filePath = dataPath + '%s 掩码.png' % version
    figure.save(mask_filePath, dpi=(254.0, 254.0))  # 生成图片
    return figure


def load_data_to_mask(version=-1, mask_figure=None):
    """
    得到元码坐标序列
    :param mask_figure:
    :return:
    """
    # 存储元码坐标
    coordinate_of_bit = []
    height, length = height_length_table[version]
    img_array = mask_figure.load()
    for i in range(2*BOUNDARY+height):
        for j in range(2*BOUNDARY+length):
            if img_array[i * BOX, j * BOX] == (255, 255, 255):
                mask_figure.putpixel((i * BOX, j * BOX), (255, 0, 0))  # 写入单个像素
                coordinate_of_bit.append((i * BOX, j * BOX))
    mask_data_figure_path = dataPath + '%s 元码点.png' % version
    mask_figure.save(mask_data_figure_path)
    return coordinate_of_bit


def return_moudle_coordinate(version=-1):
    """
    主函数
    :param version:
    :return: moudle_figure、coordinate
    """
    moudle_fig = moudle_figure(version=version)
    import copy
    target_fig = copy.deepcopy(moudle_fig)
    mask_fig = draw_mask(figure=moudle_fig, version=version)
    coordinate_of_bit = load_data_to_mask(version=version, mask_figure=mask_fig)
    print("生成模板和填充坐标： ", target_fig, coordinate_of_bit)
    return target_fig, coordinate_of_bit


if __name__ == "__main__":
    d = []
    for i in range(1, 12, 1):
        version = i
        figure = moudle_figure(version=version)
        figure = draw_mask(figure=figure, version=version)
        coordinate_of_bit = load_data_to_mask(version=version,
                                                         mask_figure=figure)
        d.append((i, (len(coordinate_of_bit) - 19) // 11 * 2))
    print(d)