# Business English Flash (BEF)

ビジネスマン向けのAI自動生成ビジネス英語カードによる学習アプリ

## 概要

Business English Flash (BEF)は、AIが自動でビジネス英語カードを生成し、1日5〜10分でビジネス英語を学習できるWebアプリケーションです。

## 機能

- AIによるカード自動生成（Google Gemini API利用）
- 音声読み上げ機能
- 復習モード
- 進捗確認
- スマホ・PC両対応

## 技術スタック

- フロントエンド: Next.js + TailwindCSS
- バックエンド: FastAPI
- AI: Google Gemini API
- 音声: Google Cloud TTS
- Docker環境

## 開発環境のセットアップ

1. リポジトリをクローン:
```
git clone <repository-url>
cd business-english-flash
```

2. .envファイルの作成:
```
cp backend/.env.example backend/.env
```
.envファイルに必要なAPIキーを設定してください。

3. Dockerで起動:
```
docker-compose up
```

4. ブラウザでアクセス:
```
http://localhost:3000
```

## テスト実行

フロントエンドのテスト:
```
cd frontend
npm test
```

バックエンドのテスト:
```
cd backend
pytest
```

## Gemini APIキーの取得方法

1. Google AI Studio (https://makersuite.google.com/) にアクセス
2. Googleアカウントでログイン
3. APIキーを取得
4. 取得したAPIキーを `backend/.env` ファイルの `GOOGLE_GEMINI_API_KEY` に設定
