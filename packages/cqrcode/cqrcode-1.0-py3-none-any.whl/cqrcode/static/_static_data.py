import os

# 数据举例
data32 = "4CJZ0maWgO6b1cotTMdjU8u3QprVkPRY"
data64 = "XFSB1wQ2XPKBsVTYdChtz9Gyx4PuYokVvbGX7ai1FYmFHRs2SDIIz39KAiGxkfxL"

# 资源路径
rawPath = os.path.abspath(__file__)
# E:\Programmer\PYTHON\cqrcode\static\
dataPath = rawPath[:rawPath.find('static')] + 'static\\'

# 只能对于 Alphanumeric_mode_table 中的字符进行编码
alphanumeric_mode_table = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15,
    'G': 16,
    'H': 17,
    'I': 18,
    'J': 19,
    'K': 20,
    'L': 21,
    'M': 22,
    'N': 23,
    'O': 24,
    'P': 25,
    'Q': 26,
    'R': 27,
    'S': 28,
    'T': 29,
    'U': 30,
    'V': 31,
    'W': 32,
    'X': 33,
    'Y': 34,
    'Z': 35,
    ' ': 36,
    '$': 37,
    '%': 38,
    '*': 39,
    '+': 40,
    '-': 41,
    '.': 42,
    '/': 43,
    ':': 44,
}
# 字符数据的 bit 值, 两个字符合起来由 11 bit表示
number_of_bits_in_character_count = 11
# 编码样式前缀 —— 字符编码
alphanumeric = '0010'
# 柱面二维码尺寸表
height_length_table = {
    1: (5, 19),
    2: (5, 29),
    3: (7, 19),
    4: (8, 18),
    5: (8, 32),
    6: (9, 29),
    7: (9, 35),
    8: (11, 35),
    9: (12, 26),
    10: (12, 36),
    11: (13, 35),
}
# 每个码元由 BOX*BOX 个像素组成
BOX = 16
# 设置边界
BOUNDARY = 1
# 每个版本的数据容量（Bytes）
CAPACITY = [(1, 6), (2, 12), (3, 10), (4, 12), (5, 30), (6, 32), (7, 40),
            (8, 52), (9, 42), (10, 62), (11, 66)]
