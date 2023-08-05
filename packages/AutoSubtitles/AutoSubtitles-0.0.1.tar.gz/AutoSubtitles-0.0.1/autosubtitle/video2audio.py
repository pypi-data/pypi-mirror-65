from moviepy.editor import VideoFileClip
import os
path = os.path.abspath('.')  # 表示当前所处的文件夹的绝对路径
path_seq = os.sep

video_file = path + path_seq + 'datasets' + path_seq + 'example_video.mp4'
audio_file = path + path_seq + 'datasets' + path_seq + 'example_audio.wav'

video = VideoFileClip(video_file)
audio = video.audio
audio.write_audiofile(audio_file)