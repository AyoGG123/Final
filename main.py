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
client_id_3 = 'fb67211eaecf49cf967e7c0bc3aeb76e'
client_secret_3 = '9425eb8ddc424d0c8064b83d1052d1f2'
client_id_4 = '8110311acd80468ea8d61c63c1c2276f'
client_secret_4 = '1d1ef322d10f403fadb49cced40adbc3'
client_id_5 = '0981062b21bf468ab1a4f4e18d32cf42'
client_secret_5 = '0010daacb89046459bdd699809322611'
scope = 'user-library-read user-read-private user-read-private user-read-email'
redirect_uri = 'http://localhost:8888/callback'
'''

# headers = get_token()

# auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

# sp = get_spotipy()

chinese_hit_50_id = '0TRuyc7C37J6p2Hg2dFMbW'  # 可用
my_playlist_id_1 = '2y05SOLfbRkjgCo3NxrTK0'  # 魔幻力量
my_playlist_id_2 = '4NGz298oXN9FqxRGhJRHmG'  # PS4歌單
hit_playlist_id = '3Me7esQS0xZkSbW0XW7roB'
SNSD_HIT_ID = '2XHQMUrtqerDns7rvl7J25'
SNSD_ALL = '5YEU5bf6TGZ53YMkBSN8RI'
koera_top_50 = '37i9dQZEVXbJZGli0rRP3r'
taiwan_top_50 = '37i9dQZEVXbMnZEatlMSiu'
usa_top_50 = '37i9dQZEVXbLRQDuF5jeBp'
japan_top_50 = '37i9dQZEVXbKXQ4mDTEBXq'
earth_top_50 = '37i9dQZEVXbMDoHDwVN2tF'
best_of_hit_chinese = '37i9dQZF1DX5KtaZhtKgCY'
best_of_hit_western = '37i9dQZF1DX3K6w77QPdGB'
best_of_hit_korean = '37i9dQZF1DWXGe6Yz1Nf9K'

hit_chinese = '3yWcDX7d2jGkdf0kDM8fUT'  # 熱門華語 2350首

top_50 = [koera_top_50, taiwan_top_50, usa_top_50, japan_top_50, earth_top_50]
best_of_hit = [best_of_hit_chinese, best_of_hit_western, best_of_hit_korean]
my_playlist_list = [my_playlist_id_2]
hit_chinese_ = [hit_chinese]

'''my_playlist = sp.current_user_saved_tracks()
my_songs_attributes = []'''

playlist_name, hit_playlist, hit_songs_attributes = list_to_attributes(list=hit_chinese_)
print("end")

for playlist, songs_attributes, name in zip(hit_playlist, hit_songs_attributes, playlist_name):
    with open(f"{name}.json", 'w') as json_file:
        json.dump(songs_attributes, json_file, indent=4)  # indent=4 用于美化输出，可选
