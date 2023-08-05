import speech_recognition as sr
# import os
# path = os.path.abspath('.')  # 表示当前所处的文件夹的绝对路径
# path_seq = os.sep
#
# audio_file = path + path_seq + 'datasets' + path_seq + 'region_16.700.wav'


def recog(audio_path):
    r = sr.Recognizer()  # 调用识别器
    test = sr.AudioFile(audio_path)  # 导入语音文件
    with test as source:
        audio = r.record(source)
    c = r.recognize_sphinx(audio)
    return c

