# -*- coding: UTF-8 -*-
import os
import time
import os
import json

ROOT = os.getcwd()

path = 'Attribute'

file_dirs = os.walk(path)

test_files = []
file_ = []

for root, dirs, files in file_dirs:
    for file in files:
        test_files.append(os.path.join(ROOT, root, file))
        '''print(f"test_files:{os.path.join(ROOT, root, file)}")
        print(f"file_names:{file}")
        print()'''

for file in test_files:
    with open(file, 'r') as json_file:  # 从 JSON 文件中读取数据
        file_.append(json.load(json_file))
        # data = json.loads(json.dumps(data, indent=4, sort_keys=True))
        # data = json.loads(json.dumps(data))

'''
這些是從Spotify API中取得的歌曲屬性（Audio Features）的資訊，這些屬性描述了特定歌曲的音樂特徵。以下是這些屬性的解釋：

danceability（舞曲性）： 歌曲適合跳舞的程度，值越高表示越容易跳舞（範圍從0到1）。
energy（能量）： 歌曲的活力和強度，值越高表示越有活力（範圍從0到1）。
key（音調）： 歌曲的音調，用數字表示，0代表C調，1代表C♯/D♭調，以此類推，共12個音調。
loudness（音量）： 歌曲的整體音量強度，以分貝（dB）表示。
mode（音階模式）： 歌曲是Major音階（1）還是Minor音階（0）。
speechiness（語音性）： 歌曲中包含語音的程度，值越高表示越多的語音元素（範圍從0到1）。
acousticness（原聲度）： 歌曲的原聲程度，值越高表示越原聲（範圍從0到1）。
instrumentalness（樂器程度）： 歌曲中是否包含樂器的程度，值越高表示越多的樂器元素（範圍從0到1）。
liveness（現場感）： 歌曲的現場表演感覺，值越高表示越像現場表演（範圍從0到1）。
valence（情感正向度）： 歌曲的情感正向度，值越高表示越正向（範圍從0到1）。
tempo（節奏）： 歌曲的節奏速度，以每分鐘的節拍數（BPM）表示。
duration_ms（歌曲持續時間）： 歌曲的持續時間，以毫秒為單位。
time_signature（拍子記號）： 歌曲的拍子記號，通常是4/4。
其他屬性是一些用於辨識和查詢歌曲的Spotify API特定資訊，如track的ID、URI、分析URL等。
'''
