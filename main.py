import spotipy
import requests
import json
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from func import *

'''
username = 'chen925069'
client_id_1 = 'd4c6646423e84b129110e8b16665e4b5'
client_secret_1 = '94353f22852e4474ae2e30348e868469'
client_id_2 = 'd65c141938284806a236cd911fd2aed0'
client_secret_2 = '6ab3a371300a48a68f2ff9ee6b770496'
scope = 'user-library-read user-read-private user-read-private user-read-email'
redirect_uri = 'http://localhost:8888/callback' 
'''

chinese_hit_50_id = '0TRuyc7C37J6p2Hg2dFMbW'  # 可用
my_playlist_id_1 = '2y05SOLfbRkjgCo3NxrTK0'  # 魔幻力量
my_playlist_id_2 = '4NGz298oXN9FqxRGhJRHmG'  # PS4
hit_playlist_id = '3Me7esQS0xZkSbW0XW7roB'
SNSD_HIT_ID = '2XHQMUrtqerDns7rvl7J25'
SNSD_ALL = '5YEU5bf6TGZ53YMkBSN8RI'
koera_top_50 = '37i9dQZEVXbJZGli0rRP3r'
taiwan_top_50 = '37i9dQZEVXbMnZEatlMSiu'
usa_top_50 = '37i9dQZEVXbLRQDuF5jeBp'
japan_top_50 = '37i9dQZEVXbKXQ4mDTEBXq'
earth_top_50 = '37i9dQZEVXbMDoHDwVN2tF'

top_50 = [koera_top_50, taiwan_top_50, usa_top_50, japan_top_50, earth_top_50]

hit_playlist = []
hit_songs_attributes = []
playlist_name = []

headers = get_token()

# auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = get_spotipy()

'''my_playlist = sp.current_user_saved_tracks()
my_songs_attributes = []'''
for id in top_50:
    playlist = sp.playlist(id)  # 從播放清單詳細信息中獲取播放清單名稱
    playlist_name.append(playlist['name'])

    a = get_playlist_tracks_(username=username, playlist_id=id, spotipy=sp)
    hit_playlist.append(a)
    # https://open.spotify.com/playlist/3Me7esQS0xZkSbW0XW7roB?si=50674079dde74588
    a = return_attributes(track_=a, headers=headers)
    hit_songs_attributes.append(a)

print("end")

for playlist, songs_attributes, name in zip(hit_playlist, hit_songs_attributes, playlist_name):
    with open(f"{name}.json", 'w') as json_file:
        json.dump(songs_attributes, json_file, indent=4)  # indent=4 用于美化输出，可选
