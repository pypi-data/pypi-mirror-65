import os

path = os.path.abspath('.')  # 表示当前所处的文件夹的绝对路径
path_seq = os.sep

video_file = path + path_seq + 'datasets' + path_seq + 'example_video.mp4'
audio_file = path + path_seq + 'datasets' + path_seq + 'example_audio.wav'

from auditok import split
# split returns a generator of AudioRegion objects
audio_regions = split(audio_file)
for region in audio_regions:
    # region.play(progress_bar=True)
    filename = region.save("./datasets/region_split/region_{meta.start:.3f}_{meta.end:.3f}.wav")
    print("region saved as: {}".format(filename))

import os
import re

for root, dirs, files in os.walk("./datasets/region_split"):
    print(files)
    no = len(files)
    with open('test.srt',"r+") as f:
        f.truncate()
    for i in range(no):
        pattern = re.compile(r'\d+.\d+')  # 查找数字
        result1 = pattern.findall(files[i])
        result = [str(i) + "\n", result1[0], ' --> ', result1[1] + "\n", "\n"]
        file_handle = open('test.srt', mode='a')
        file_handle.writelines(result)
        file_handle.close()