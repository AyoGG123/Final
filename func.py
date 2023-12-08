import sys
import spotipy
import requests
import json
import time
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

'''
set SPOTIPY_CLIENT_ID='d4c6646423e84b129110e8b16665e4b5'
set SPOTIPY_CLIENT_SECRET='94353f22852e4474ae2e30348e868469'
set SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'
'''

'''
dict_keys(
    ['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit', 'external_ids', 'external_urls',
     'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track_number', 'type', 'uri'])
'''

username = 'chen925069'
client_id_1 = 'd4c6646423e84b129110e8b16665e4b5'
client_secret_1 = '94353f22852e4474ae2e30348e868469'
client_id_2 = 'd65c141938284806a236cd911fd2aed0'
client_secret_2 = '6ab3a371300a48a68f2ff9ee6b770496'
client_id_3 = 'fb67211eaecf49cf967e7c0bc3aeb76e'
client_secret_3 = '9425eb8ddc424d0c8064b83d1052d1f2'
scope = 'user-library-read user-read-private user-read-private user-read-email'
redirect_uri = 'http://localhost:8888/callback'

client_id = client_id_3
client_secret = client_secret_3


def get_spotipy():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))
    return sp


def get_token():
    # token 你的token，在运行上面的代码后，会显示在http://localhost/里面
    auth_url = 'https://accounts.spotify.com/api/token'

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    auth_response = requests.post(auth_url, data=data)
    access_token = auth_response.json().get('access_token')

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    headers = {key: value.encode('utf-8') for key, value in headers.items()}
    # print(access_token)
    return headers


def get_song_attributes(response_text):
    if response_text:
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print("Empty response or non-JSON content")


def get_playlist_tracks_(username, playlist_id, spotipy):
    offset = 0
    limit = 100
    tracks = []

    while True:
        results = spotipy.user_playlist_tracks(user=username, playlist_id=playlist_id, fields=None, limit=limit,
                                               offset=offset, market=None)

        for track in results['items']:
            tracks.append(track)

        offset += limit
        next = results['next']
        time.sleep(10)
        if next is None:
            break

    return tracks


def return_attributes(track_, headers):
    _songs_attributes = []
    for idx, item in enumerate(track_):
        while True:
            track = item['track']
            song_attributes = requests.get(f"https://api.spotify.com/v1/audio-features/{track['id']}", headers=headers)

            if song_attributes.status_code == 429:
                # 如果標頭中包含Retry-After，則獲取其值
                retry_after = song_attributes.headers.get('Retry-After')
                if retry_after:
                    time.sleep(eval(retry_after) + 1)
                    print(f"服務器建議等待 {retry_after} 秒再試一次。")
                else:
                    time.sleep(5)
                    print("服務器建議等待，但未提供確切的時間。")
                    sys.exit()
                continue

            _songs_attributes.append(get_song_attributes(song_attributes.text))
            print(f"{idx} {track['artists'][0]['name']} - {track['name']}")
            print(song_attributes.text)
            break
    return _songs_attributes


def list_to_attributes(sp, headers, list):
    hit_playlist = []
    hit_songs_attributes = []
    playlist_name = []

    for id in list:
        playlist = sp.playlist(id)  # 從播放清單詳細信息中獲取播放清單名稱
        playlist_name.append(playlist['name'])

        a = get_playlist_tracks_(username=username, playlist_id=id, spotipy=sp)
        hit_playlist.append(a)
        # https://open.spotify.com/playlist/3Me7esQS0xZkSbW0XW7roB?si=50674079dde74588
        a = return_attributes(track_=a, headers=headers)
        hit_songs_attributes.append(a)
    return playlist_name, hit_playlist, hit_songs_attributes


if __name__ == "__main__":
    pass
