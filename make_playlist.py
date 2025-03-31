import google_oauth as go

from googleapiclient.discovery import build
import json

# config.jsonから設定を読み込む
with open('APIKeys/config.json', 'r') as config_file:
    config = json.load(config_file)

YOUTUBE_API_SERVICE_NAME = config["YOUTUBE_API_SERVICE_NAME"]
YOUTUBE_API_VERSION = config["YOUTUBE_API_VERSION"]
YOUTUBE_API_KEY = config["YOUTUBE_API_KEY"]

youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=YOUTUBE_API_KEY)

CLIENT_SECRET_FILE = "APIKeys/client_secret.json"
SCOPE = ["https://www.googleapis.com/auth/youtube"]   # YouTube APIのスコープ

# 空のプレイリストを作成する関数
def make_playlist(youtube, playlist_title):
    responce = youtube.playlists().insert(
        part="snippet,status",
        body=dict(
            snippet=dict(
                title=playlist_title,
                description="A private playlist created with the YouTube API v3"
            ),
            status=dict(
                privacyStatus="private"
            )
        )
    ).execute()
    print(responce["id"])  #playlistid

    return responce["id"]   # 作成したプレイリストのIDを返す

# プレイリストに楽曲を追加する関数
def add_to_playlist(youtube, playlistid, videoid):
    response = youtube.playlistItems().insert(
        part="snippet",
        body=dict(
            snippet=dict(
                playlistId=playlistid,
                resourceId=dict(
                    kind="youtube#video",
                    videoId=videoid
                )
            )
        )
    ).execute()
    print(response)
    