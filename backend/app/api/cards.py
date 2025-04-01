# backend/app/api/cards.py
from fastapi import APIRouter, HTTPException, Depends
from models.card import ThemeRequest, CardsResponse, Card
from services.ai_service import generate_cards
from services.tts_service import generate_audio
from typing import List
import uuid

router = APIRouter()

@router.post("/generate-cards", response_model=CardsResponse)
async def create_cards(request: ThemeRequest):
    """
    テーマに基づいてビジネス英語カードを生成するエンドポイント
    """
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