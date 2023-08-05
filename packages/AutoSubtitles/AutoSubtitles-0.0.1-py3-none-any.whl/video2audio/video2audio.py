from moviepy.editor import VideoFileClip

# get the audio from the video
def get_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)