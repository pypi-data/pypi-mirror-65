# coding: utf-8 
# !/usr/bin/python
"""
@File       :   __init__.py.py
@Author     :   jiaming
@Modify Time:   2020/4/2 19:15    
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   None
"""
from cqrcode.view.GUI_welcome import hello

while True:
    x = input(
        """type 's' to start...（figures save in .../cqrcode/static/）\n""")
    if x == 's' or x == 'S':
        hello()
    else:
        break