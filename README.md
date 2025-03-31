# CSVからYouTubeプレイリスト自動生成ツール

## 概要

このツールは、CSVファイルに記載された楽曲リスト（アーティスト名と曲名）を元に、YouTubeで動画を検索し、自動で非公開のプレイリストを作成します。
作成したプレイリストはYouTube及びYouTube Musicで利用することができます。
(本ツールは主にミュージックビデオの検索とプレイリストの作成に利用することを想定しています。)

## 機能

*   CSVファイルからアーティスト名と曲名を読み込みます。
*   YouTube Data API v3 を使用して、各楽曲に対応する動画を検索します。
*   Google OAuth 2.0 認証を使用して、ユーザーのYouTubeアカウントにアクセスします。
*   認証されたアカウントで新しい非公開プレイリストを作成します。
*   検索で見つかった動画を順番にプレイリストに追加します。
*   作成されたプレイリストのURLを出力します。

## 必要なもの

*   Python 3.x
*   Google Cloud Platform (GCP) アカウント
*   楽曲リストが記載されたCSVファイル (`playlist_data.csv`)

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2. 環境構築

#### 通常のPython環境の場合

必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

#### Docker環境の場合

Docker と Docker Compose がインストールされている必要があります。

```bash
docker-compose build
docker-compose run --rm docker_python bash
```
（コンテナ内で以降の操作を行います）

### 3. Google Cloud Platformでの設定

このツールを使用するには、Google Cloud Platform (GCP) でプロジェクトを作成し、以下のAPIキーと認証情報を取得する必要があります。

1.  **GCPプロジェクトの作成**:
    *   [Google Cloud Console](https://console.cloud.google.com/) にアクセスし、新しいプロジェクトを作成します。

2.  **YouTube Data API v3 の有効化**:
    *   作成したプロジェクトのダッシュボードで、「APIとサービス」>「ライブラリ」に移動します。
    *   「YouTube Data API v3」を検索し、有効にします。

3.  **APIキーの作成**:
    *   「APIとサービス」>「認証情報」に移動します。
    *   「認証情報を作成」をクリックし、「APIキー」を選択します。
    *   作成されたAPIキーをコピーします。
    *   プロジェクトのルートディレクトリに `APIKeys` というディレクトリを作成します。
    *   `APIKeys` ディレクトリ内に `config.json` というファイルを作成し、以下の形式でAPIキーを記述します。

    ```json:APIKeys/config.json
    {
        "YOUTUBE_API_SERVICE_NAME": "youtube",
        "YOUTUBE_API_VERSION": "v3",
        "YOUTUBE_API_KEY": "ここにコピーしたAPIキーを貼り付け"
    }
    ```

4.  **OAuth 2.0 クライアント ID の作成**:
    *   「APIとサービス」>「認証情報」に移動します。
    *   「認証情報を作成」をクリックし、「OAuth クライアント ID」を選択します。
    *   「同意画面を設定」を求められた場合は、指示に従って設定します（「外部」を選択し、テストユーザーとして自分のGoogleアカウントを追加するなど）。
    *   アプリケーションの種類として「デスクトップ アプリ」を選択します。
    *   クライアントIDに任意の名前を付け、「作成」をクリックします。
    *   作成されたクライアントIDとクライアントシークレットが表示されるので、「JSONをダウンロード」をクリックします。
    *   ダウンロードしたJSONファイルを `client_secret.json` という名前で `APIKeys` ディレクトリに保存します。

    **注意:** `APIKeys` ディレクトリとその中のファイル (`config.json`, `client_secret.json`) は `.gitignore` に含まれており、Gitリポジトリにはコミットされません。これらのファイルは安全な場所に保管してください。

### 4. CSVファイルの準備

プロジェクトのルートディレクトリに `playlist_data.csv` という名前のCSVファイルを作成します。ファイルはUTF-8エンコーディングで保存し、以下のような形式で記述します。1行目はヘッダー行とします。

```csv:playlist_data.csv
Artist,Song
アーティストA,曲名1
アーティストB,曲名2
,曲名3
アーティストC,
```
*   1列目にアーティスト名、2列目に曲名を記述します。
*   アーティスト名が不明な場合は空欄にします（曲名のみで検索されます）。
*   曲名が不明な場合はその行はスキップされます。

## 使い方

1.  必要な設定ファイル (`APIKeys/config.json`, `APIKeys/client_secret.json`) と `playlist_data.csv` を配置します。
2.  `create_playlist_from_csv.py` を実行します。

    ```bash
    python create_playlist_from_csv.py
    ```

3.  初回実行時には、ブラウザが起動しGoogleアカウントの認証を求められます。画面の指示に従って、プレイリスト作成を許可するアカウントでログインし、権限を許可してください。
    *   認証が成功すると、アクセストークンが `token.json` として保存され、次回以降は自動的に使用されます。
4.  スクリプトが実行され、CSVファイルの各行について動画検索とプレイリストへの追加が行われます。
5.  処理が完了すると、作成されたYouTubeプレイリストのURLが表示されます。

## 注意事項

*   YouTube Data API v3 には無料利用枠のクォータ（利用上限）があります。大量の楽曲を含むCSVファイルを処理する場合、クォータ上限に達する可能性があります。
*   動画検索は、アーティスト名と曲名を組み合わせたキーワードで行われます。検索結果の精度はキーワードによって変動します。このスクリプトでは、最初に見つかった動画をプレイリストに追加します。
*   作成されるプレイリストはデフォルトで「非公開」設定になっています。
*   本プログラムを利用して発生した不利益について、作成者は一切の責任を負いません。利用は自己責任でお願いいたします。

<!-- ## ライセンス

(必要であればライセンス情報を記載してください。例: MIT License) -->