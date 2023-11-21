import spotipy
import requests
import json
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from func import *

'''
username = 'chen925069'
client_id = 'd4c6646423e84b129110e8b16665e4b5'
client_secret = '94353f22852e4474ae2e30348e868469'
scope = 'user-library-read user-read-private user-read-private user-read-email'
redirect_uri = 'http://localhost:8888/callback' 
'''

chinese_hit_50_id = '0TRuyc7C37J6p2Hg2dFMbW'  # 可用
my_playlist_id_1 = '2y05SOLfbRkjgCo3NxrTK0'  # 魔幻力量
my_playlist_id_2 = '4NGz298oXN9FqxRGhJRHmG'  # PS4
hit_playlist_id = '3Me7esQS0xZkSbW0XW7roB'
SNSD_HIT_ID = '2XHQMUrtqerDns7rvl7J25'
SNSD_ALL = '5YEU5bf6TGZ53YMkBSN8RI'

headers = get_token()

# auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = get_spotipy()

'''my_playlist = sp.current_user_saved_tracks()
my_songs_attributes = []'''

hit_playlist = get_playlist_tracks_(username=username, playlist_id=SNSD_ALL, spotipy=sp)
# https://open.spotify.com/playlist/3Me7esQS0xZkSbW0XW7roB?si=50674079dde74588
hit_songs_attributes = return_attributes(track_=hit_playlist, headers=headers)
