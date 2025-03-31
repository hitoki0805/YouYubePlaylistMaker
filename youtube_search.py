import json

from googleapiclient.discovery import build  
#公式ではapiclient.discoveryだがVSCodeの補完を働かせるために変更

# config.jsonから設定を読み込む
with open('APIKeys/config.json', 'r') as config_file:
    config = json.load(config_file)

YOUTUBE_API_SERVICE_NAME = config["YOUTUBE_API_SERVICE_NAME"]
YOUTUBE_API_VERSION = config["YOUTUBE_API_VERSION"]
YOUTUBE_API_KEY = config["YOUTUBE_API_KEY"]

youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=YOUTUBE_API_KEY)

def youtube_search(youtube, word):
    response = youtube.search().list(part="snippet",
                                     q=word,
                                     type="video",
                                     videoCategoryId="10"  # videoCategoryIdもstr型
                                     ).execute()
    print(type(response))  # <class 'dict'>
    first_video_id = None
    for index, item in enumerate(response.get('items', [])):
        print(item["snippet"]["title"], item["id"]["videoId"])
        if index == 0:
            first_video_id = item["id"]["videoId"]  # 一番最初にヒットした動画のidを保存

            return first_video_id   # とりあえず1つ目の動画のidを返すように変更(容易にAPIの実行回数の上限に達するため)
    # return first_video_id  # 一番最初にヒットした動画のidを返す
