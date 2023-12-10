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
client_id_4 = '8110311acd80468ea8d61c63c1c2276f'
client_secret_4 = '1d1ef322d10f403fadb49cced40adbc3'
client_id_5 = '0981062b21bf468ab1a4f4e18d32cf42'
client_secret_5 = '0010daacb89046459bdd699809322611'
scope = 'user-library-read user-read-private user-read-private user-read-email'
redirect_uri = 'http://localhost:8888/callback'

client_id_list = [client_id_1, client_id_2, client_id_3, client_id_4, client_id_5]
client_secret_list = [client_secret_1, client_secret_2, client_secret_3, client_secret_4, client_secret_5]

client_id = client_id_1
client_secret = client_secret_1


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


def return_attributes(track_, headers, _songs_attributes, idx_index=0):
    # _songs_attributes = []

    for idx, item in enumerate(track_[idx_index:]):
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
                    print("服務器建議等待，但未提供確切的時間。")
                    print(f"已return 在idx={idx + idx_index}失敗 更換token")
                    return _songs_attributes, True, idx + idx_index
                continue

            _songs_attributes.append(get_song_attributes(song_attributes.text))
            print(f"{idx + idx_index} {track['artists'][0]['name']} - {track['name']}")
            print(song_attributes.text)
            break

    return _songs_attributes, False, len(track_)


def list_to_attributes(list):
    headers = get_token()
    sp = get_spotipy()

    hit_playlist = []
    hit_songs_attributes = []
    playlist_name = []
    i = 1

    for id in list:
        playlist = sp.playlist(id)  # 從播放清單詳細信息中獲取播放清單名稱
        playlist_name.append(playlist['name'])

        tracks = get_playlist_tracks_(username=username, playlist_id=id, spotipy=sp)
        hit_playlist.append(tracks)

        a, flag, idx_index = return_attributes(track_=tracks, headers=headers, _songs_attributes=[], idx_index=0)

        while flag:
            if i == len(client_id_list):
                print(f"在{playlist_name[len(playlist_name) - 1]} idx_index={idx_index} 遇到異常")
                break

            client_id = client_id_list[i]
            client_secret = client_secret_list[i]
            i += 1

            headers = get_token()
            sp = get_spotipy()

            a, flag, idx_index = return_attributes(track_=tracks, headers=headers, _songs_attributes=a,
                                                   idx_index=idx_index)

    hit_songs_attributes.append(a)

    return playlist_name, hit_playlist, hit_songs_attributes


if __name__ == "__main__":
    pass
