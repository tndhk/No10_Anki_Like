# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# サービスモジュール
from services.ai_service import generate_cards
from services.tts_service import generate_audio

# 環境変数のロード
load_dotenv()

app = FastAPI(title="Business English Flash API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのオリジン
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストモデル
class ThemeRequest(BaseModel):
    theme: str

# レスポンスモデル
class Card(BaseModel):
    id: str
    phrase: str
    example: str
    translation: str
    situation: str
    audio_url: str = None

class CardsResponse(BaseModel):
    cards: List[Card]

@app.get("/")
def read_root():
    return {"message": "Welcome to Business English Flash API"}

@app.post("/api/generate-cards", response_model=CardsResponse)
async def create_cards(request: ThemeRequest):
    if not request.theme:
        raise HTTPException(status_code=400, detail="Theme cannot be empty")
    
    try:
        # AIを使ってカードを生成
        cards = generate_cards(request.theme)
        
        # 各カードにオーディオURLを追加
        for card in cards:
            audio_path = await generate_audio(card["phrase"])
            card["audio_url"] = audio_path
        
        return {"cards": cards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# アプリの起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
