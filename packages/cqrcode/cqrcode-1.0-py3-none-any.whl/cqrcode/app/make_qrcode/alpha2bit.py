# coding: utf-8
# !/usr/bin/python
"""
@File       :   alpha2bit.py
@Author     :   jiaming
@Modify Time:   2020/4/2 20:28
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   集合了字符编码解码函数调用
                只能对于 Alphanumeric_mode_table 中的字符进行编码
"""
from cqrcode.static._static_data import number_of_bits_in_character_count, \
    alphanumeric_mode_table, alphanumeric
import random


def data_encode(alpha=''):
    """
    对传入原生字符串进行检查并编码为一份标准填充比特流。
    :param alpha: Alphanumeric_mode_table 表中的字符
    :return: 原生字符对应的填充比特流
    """
    alpha = alpha.upper()
    alpha_group = ''
    results = ''  # 保存最终比特流

    # 对于原生字符，两两成组，转换为 11 bit
    for i in range(0, len(alpha) - 1, 2):
        alpha_group += alpha[i] + alpha[i + 1] + ' '
        number = alphanumeric_mode_table[alpha[i]] * 45 + \
            alphanumeric_mode_table[alpha[i + 1]]
        bits = ''.join(list(bin(number))[2:])
        # 不够 11 bit， 用 0 补齐。
        if len(bits) < 11:
            bits = '0' * (11 - len(bits)) + bits  # 得到原始数据
        results += bits + ' '

    # 对于落单的字符单独编成 6 bit 数据
    if len(alpha) % 2 != 0:
        alpha_group += alpha[-1]
        number = alphanumeric_mode_table[alpha[-1]]
        bits = ''.join(list(bin(number))[2:])
        if len(bits) < 6:
            bits = '0' * (6 - len(bits)) + bits  # 得到原始数据
        results += bits + ' '

    number_of_bits = ''.join(list(bin(len(alpha)))[2:])
    if len(number_of_bits) < number_of_bits_in_character_count:
        number_of_bits = '0' * \
            (number_of_bits_in_character_count - len(number_of_bits)) + number_of_bits
    print('消除空格前编码后数据： ', alphanumeric + ' ' + number_of_bits + ' ' + results +
          '0000')
    data_bits = (alphanumeric + ' ' + number_of_bits + ' ' + results +
                 '0000').replace(' ', '')
    print('消除空格后编码后数据: ', data_bits)
    return data_bits


def random_bit(length=-1):
    """
    返回 length 长度的比特流
    :param length:
    :return:
    """

    return ''.join([random.choice(['1', '0']) for i in range(length)])


if __name__ == "__main__":
    print(random_bit(10))
