# -*- coding: UTF-8 -*-
import os
import json
import pandas as pd
import numpy as np

ROOT = os.getcwd()
attribute_path = 'Attribute'
my_playlist_file_path = 'myplaylist'
all_path = 'all_in_one'

file_dirs = os.walk(attribute_path)
my_playlist_file_dirs = os.walk(my_playlist_file_path)
all_dirs = os.walk(all_path)


def get_file(dirs):
    test_files = []
    file_ = []
    for root, dirs, files in dirs:
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
    return file_


def get_songs_df(file_):
    # 合併所有 JSON 檔的歌曲屬性資料
    all_songs = []
    for data in file_:
        for item in data:
            song_info = {
                'uri': item.get('uri', None),
                'danceability': item.get('danceability', None),
                'energy': item.get('energy', None),
                'valence': item.get('valence', None),
                'tempo': item.get('tempo', None),
                # 其他屬性依需求加入
            }
            all_songs.append(song_info)

    # 建立 DataFrame
    return pd.DataFrame(all_songs)


def playlist_average_preferences(songs_df):
    return {'danceability': songs_df['danceability'].mean(),
            'energy': songs_df['energy'].mean(),
            'valence': songs_df['valence'].mean()}


def merge_attribute(source_path, target_path):
    file_ = get_file(file_dirs)
    all_songs = []

    for data in file_:
        for item in data:
            all_songs.append(item)

    print(f"all_songs：{len(all_songs)}")
    unique_data = list({item['id']: item for item in all_songs}.values())
    print(f"unique_data：{len(unique_data)}")
    json_data = json.dumps(unique_data, indent=4)  # indent=4 是為了美觀的格式化

    # 將 JSON 資料寫入新的檔案
    with open(f'{target_path}/all.json', 'w') as file:
        file.write(json_data)


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

if __name__ == "__main__":
    # merge_attribute(source_path=attribute_path, target_path=all_path)

    file_ = get_file(file_dirs)
    my_playlist_file_ = get_file(my_playlist_file_dirs)
    all_ = get_file(all_dirs)  # 不重複的

    # 建立 DataFrame
    db_df = get_songs_df(file_)
    my_df = get_songs_df(my_playlist_file_)
    all_df = get_songs_df(all_)  # 不重複的

    # 顯示 DataFrame 的前幾行
    print(all_df.head())

    # 進行一些簡單的分析
    print("\n平均舞曲性 (Danceability):", all_df['danceability'].mean())
    print("平均能量 (Energy):", all_df['energy'].mean())
    print("平均情感正向度 (Valence):", all_df['valence'].mean())

    '''# 顯示某些統計資訊
    print("\n資料描述:")
    print(all_df.describe())'''

    # 用戶的偏好
    user_preferences = playlist_average_preferences(my_df)
    print(user_preferences)

    # 計算歐氏距離
    all_df['distance'] = np.sqrt((all_df['danceability'] - user_preferences['danceability']) ** 2 +
                                 (all_df['energy'] - user_preferences['energy']) ** 2)

    # 根據距離排序並選擇最接近的歌曲
    recommended_songs = all_df.sort_values(by='distance').head(10)[['uri', 'danceability', 'energy']]
    print(recommended_songs)
