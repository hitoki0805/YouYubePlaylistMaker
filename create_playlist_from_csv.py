import csv
import json
from googleapiclient.discovery import build  

# プログラムのインポート
import make_playlist as mp
import youtube_search as ys
import google_oauth as go

# config.jsonから設定を読み込む
with open('APIKeys/config.json', 'r') as config_file:
    config = json.load(config_file)

YOUTUBE_API_SERVICE_NAME = config["YOUTUBE_API_SERVICE_NAME"]
YOUTUBE_API_VERSION = config["YOUTUBE_API_VERSION"]
YOUTUBE_API_KEY = config["YOUTUBE_API_KEY"]

CLIENT_SECRET_FILE = "APIKeys/client_secret.json"
SCOPE = ["https://www.googleapis.com/auth/youtube"]   # YouTube APIのスコープ

creds = go.OAuth_credentials(CLIENT_SECRET_FILE, SCOPE)
youtube_oauth = build("youtube", "v3", credentials=creds)
youtube_api = build(YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=YOUTUBE_API_KEY)

def process_csv_for_playlist(csv_file_path):
    search_words = []
    # CSVファイルを読み込む
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # ヘッダーをスキップ
        next(csv_reader)
        
        # CSVの各行を処理
        for row in csv_reader:
            artist = row[0].strip()
            song = row[1].strip()
            if artist and song:
                search_word = f"{artist} {song}"
            elif song:
                search_word = song
            else:
                continue
            search_words.append(search_word)
    
    return search_words

if __name__ == '__main__':
    # CSVファイルのパスを指定
    csv_file_path = 'playlist_data.csv'
    search_words = process_csv_for_playlist(csv_file_path)
    # print(search_words)

    song_id_list = []    # プレイリストに追加する楽曲のIDのリスト
    # search_wordsリストの各要素に対して処理を行う
    for search_word in search_words:
        print(f"検索ワード: {search_word}")
        song_id = ys.youtube_search(youtube_api, search_word)
        song_id_list.append(song_id)

    print(song_id_list)
    print(f"song_id_listの長さ:{len(song_id_list)}")

    playlist_id = mp.make_playlist(youtube_oauth, "your_playlist_name")

    for song_id in song_id_list:
        print(song_id)
        mp.add_to_playlist(youtube_oauth, playlist_id, song_id)

    # プレイリストのURLを生成
    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
    print(f"Playlist URL: {playlist_url}")