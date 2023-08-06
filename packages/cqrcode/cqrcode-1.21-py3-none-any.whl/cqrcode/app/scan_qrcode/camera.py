# encoding:utf-8
"""
控制摄像头进行抓取拍照
"""
# linux
# from picamera import PiCamera
from time import sleep
from cqrcode.static._static_data import dataPath


def take_photo(pixel=(500, 500)):
    """
    控制摄像头进行抓取拍照
    :param pixel: 输出的图片尺寸
    :return: filePath = dataPath + r'/capture_qrcode.jpg'
    """
    camera = PiCamera()
    camera.resolution = pixel  # 照片的最大分辨率时2592x1944，视频的最大分辨率为1920x1080
    # camera.framerate = 15  # 帧速率
    camera.brightness = 48  # 改变亮度设置，范围是0-100，预设为50
    filePath = dataPath + r'/capture_qrcode.png'
    print("capturing...don't move! (3s)")
    # camera.start_preview()
    sleep(3)  # 捕获图片前，至少要给传感器两秒钟时间感光
    camera.capture(filePath)
    # camera.stop_preview()
    print('done...')
    camera.close()
    return filePath


if __name__ == "__main__":
    take_photo()
