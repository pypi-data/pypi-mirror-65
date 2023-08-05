import speech_recognition as sr
import os
import math

path = os.path.abspath('.')  # 表示当前所处的文件夹的绝对路径
path_seq = os.sep
import pysrt

import time

timeArray = time.localtime(1160.700)  # 秒数
otherStyleTime = time.strftime("%H:%M:%S", timeArray)
print(otherStyleTime)


def make_readable(seconds):
    hours, a = divmod(seconds, 3600)
    minutes, a = divmod(a, 60)
    milliseconds,seconds = math.modf(a)
    return '%d:%d:%d,%d' % (hours, minutes, seconds, milliseconds*1000)


t = make_readable(1160.700)
print(t)
