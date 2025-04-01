// src/types/card.ts
export interface Card {
  id: string;
  phrase: string;
  example: string;
  translation: string;
  situation: string;
  audio_url?: string;
  reviewed?: boolean;
}

export interface CardsResponse {
  cards: Card[];
}
