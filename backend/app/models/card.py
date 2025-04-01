# backend/app/models/card.py
from pydantic import BaseModel
from typing import List, Optional

class Card(BaseModel):
    id: str
    phrase: str
    example: str
    translation: str
    situation: str
    audio_url: Optional[str] = None

class CardsResponse(BaseModel):
    cards: List[Card]

class ThemeRequest(BaseModel):
    theme: str