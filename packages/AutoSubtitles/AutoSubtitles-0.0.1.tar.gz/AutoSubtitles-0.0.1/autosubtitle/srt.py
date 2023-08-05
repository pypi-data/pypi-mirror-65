import pysrt
import configs
import time


from googletrans import Translator


def google_translate(text, dest_lan, src_lan="auto"):
    translator = Translator(service_urls=['translate.google.cn'])
    return translator.translate(text, dest=dest_lan, src=src_lan).text



subs = pysrt.open(configs.srt_path)

for i in range(len(subs)):
    src_text = subs[i].text
    dest_text = google_translate(src_text,dest_lan="zh-cn")
    subs[i].text = dest_text
    time.sleep(2)

subs.save(configs.dest_srt_path, encoding='utf-8')
