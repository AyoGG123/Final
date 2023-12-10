import sqlite3
import os
from Attribute_analysis import get_file


def createDatabase():
    conn = sqlite3.connect(f"database/jsonToDatabase.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            danceability REAL,
            energy REAL,
            key INTEGER,
            loudness REAL,
            mode INTEGER,
            speechiness REAL,
            acousticness REAL,
            instrumentalness REAL,
            liveness REAL,
            valence REAL,
            tempo REAL,
            type TEXT,
            track_id TEXT,
            uri TEXT,
            track_href TEXT,
            analysis_url TEXT,
            duration_ms INTEGER,
            time_signature INTEGER)''')
    conn.commit()
    conn.close()


def json_into_db(file):
    conn = sqlite3.connect(f"database/jsonToDatabase.db")
    cursor = conn.cursor()
    for data in file:
        for item in data:
            # 檢查是否存在相同紀錄
            cursor.execute('''
                INSERT OR REPLACE INTO songs (danceability, energy, key, loudness, mode, 
                    speechiness, acousticness, instrumentalness, liveness, valence, 
                    tempo, type, track_id, uri, track_href, 
                    analysis_url, duration_ms, time_signature)
                SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM songs
                    WHERE track_id = ?
                )
            ''', (
                item.get('danceability', None),
                item.get('energy', None),
                item.get('key', None),
                item.get('loudness', None),
                item.get('mode', None),
                item.get('speechiness', None),
                item.get('acousticness', None),
                item.get('instrumentalness', None),
                item.get('liveness', None),
                item.get('valence', None),
                item.get('tempo', None),
                item.get('type', None),
                item.get('id', None),
                item.get('uri', None),
                item.get('track_href', None),
                item.get('analysis_url', None),
                item.get('duration_ms', None),
                item.get('time_signature', None),
                item.get('id', None)  # 使用 track_id 進行比對
            ))

            # 檢查是否插入成功
            cursor.execute('SELECT changes()')
            if cursor.fetchone()[0] > 0:
                pass
                # print(f"已添加: {data}")
            else:
                pass
                # print(f"重複內容跳過 (duplicate): {data}")

    conn.commit()
    conn.close()


attribute_path = 'Attribute'
all_path = 'all_in_one'

file_dirs = os.walk(attribute_path)
file_ = get_file(file_dirs)

createDatabase()
json_into_db(file_)
