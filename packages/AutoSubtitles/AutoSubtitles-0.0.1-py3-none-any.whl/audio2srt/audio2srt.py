from auditok import split
import math
import os
import re
import speech_recognition as sr
import pysrt
import time
from googletrans import Translator


# split the audio returns a generator of AudioRegion objects
def split_audio(audio_path, split_audio_path):
    split_audio_file = split_audio_path + os.sep + "audio_split_{meta.start:.3f}_{meta.end:.3f}.wav"
    audio_regions = split(audio_path)
    for region in audio_regions:
        # region.play(progress_bar=True)
        if os.path.exists(split_audio_path):
            filename = region.save(split_audio_file)
            print("audio_split saved as: {}".format(filename))
        else:
            os.mkdir(split_audio_path)
            filename = region.save(split_audio_file)
            print("audio_split saved as: {}".format(filename))


def google_translate(text, dest_lan, src_lan="auto"):
    translator = Translator(service_urls=['translate.google.cn'])
    return translator.translate(text, dest=dest_lan, src=src_lan).text


def translate_srt(srt_path, dest_srt_path, dest_lan, src_lan="auto"):
    subs = pysrt.open(srt_path)
    for i in range(len(subs)):
        src_text = subs[i].text
        dest_text = google_translate(src_text, dest_lan=dest_lan, src_lan=src_lan)
        subs[i].text = dest_text
        time.sleep(2)
    subs.save(dest_srt_path, encoding='utf-8')


def translate_time(seconds):
    hours, a = divmod(seconds, 3600)
    minutes, a = divmod(a, 60)
    milliseconds, seconds = math.modf(a)
    return '%d:%d:%d,%d' % (hours, minutes, seconds, milliseconds * 1000)


# speech recognition
def speech_recognition(audio_path):
    r = sr.Recognizer()  # 调用识别器
    audio_file = sr.AudioFile(audio_path)  # 导入语音文件
    with audio_file as source:
        audio = r.record(source)
    words = r.recognize_sphinx(audio)
    return words


# generate the video's srt file
def write_srt(split_audio_path, srt_path):
    for root, dirs, files in os.walk(split_audio_path):
        print(files)
    audio_nums = len(files)
    if os.path.exists(srt_path):
        with open(srt_path, "r+") as f:
            f.truncate()
    else:
        with open(srt_path, "w+") as f:
            f.close()
    for no in range(audio_nums):
        pattern = re.compile(r'\d+.\d+')  # 查找数字
        result1 = pattern.findall(files[no])
        try:
            words = speech_recognition(split_audio_path + os.sep + files[no])
            print("%d words %s!" % (no, words))
        except:
            print("%d Error %s" % (no, files[no]))
            words = "Error" + files[no]
        result = [str(no) + "\n", translate_time(float(result1[0])), ' --> ', translate_time(float(result1[1])) + "\n",
                  words + "\n", "\n"]
        file_handle = open(srt_path, mode='a')
        file_handle.writelines(result)
        file_handle.close()