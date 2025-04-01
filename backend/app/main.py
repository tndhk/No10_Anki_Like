# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# APIルーターのインポート
from api.cards import router as cards_router

# 環境変数のロード
load_dotenv()

app = FastAPI(title="Business English Flash API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],  # フロントエンドのオリジン
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイルの提供
app.mount("/static", StaticFiles(directory="static"), name="static")

# APIルーターの登録
app.include_router(cards_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Business English Flash API"}

# アプリの起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)