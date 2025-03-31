import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

CLIENT_SECRET_FILE = "APIKeys/client_secret.json"
SCOPE = ["https://www.googleapis.com/auth/youtube"]   # YouTube APIのスコープ


def OAuth_credentials(client_secret_file, scopes, token_storage="token.json"):
    creds = None
    # 2回目以降は既存アクセストークンを使用
    if os.path.exists(token_storage):
        creds = Credentials.from_authorized_user_file(token_storage, scopes)

    # 初回認証時処理
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, scopes=scopes)
            creds = flow.run_local_server(port=0)
            if creds is None:
                raise RuntimeError("認証フローが完了しませんでした。")

        # アクセストークンを保存
        with open(token_storage, 'w') as token:
            token.write(creds.to_json())

    return creds
