// src/app/store/cards.ts
'use client';

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Card } from '@/types/card';

interface CardsState {
  cards: Card[];
  currentCardIndex: number;
  reviewedCount: number;
  newCount: number;
  setCards: (cards: Card[]) => void;
  markAsReviewed: (cardId: string) => void;
  nextCard: () => void;
  previousCard: () => void;
  resetProgress: () => void;
}

export const useCardsStore = create<CardsState>()(
  persist(
    (set, get) => ({
      cards: [],
      currentCardIndex: 0,
      reviewedCount: 0,
      newCount: 0,
      
      setCards: (cards) => set({ 
        cards, 
        currentCardIndex: 0,
        reviewedCount: 0,
        newCount: 0
      }),
      
      markAsReviewed: (cardId) => {
        const { cards, reviewedCount, newCount } = get();
        const updatedCards = cards.map(card => 
          card.id === cardId && !card.reviewed 
            ? { ...card, reviewed: true } 
            : card
        );
        
        // カードが初めてレビューされた場合のみカウントを更新
        const cardWasNew = cards.find(card => card.id === cardId)?.reviewed === undefined;
        const cardWasReviewed = cards.find(card => card.id === cardId)?.reviewed === true;
        
        set({ 
          cards: updatedCards,
          reviewedCount: cardWasNew || !cardWasReviewed ? reviewedCount + 1 : reviewedCount,
          newCount: cardWasNew ? newCount + 1 : newCount
        });
      },
      
      nextCard: () => {
        const { currentCardIndex, cards } = get();
        if (currentCardIndex < cards.length - 1) {
          set({ currentCardIndex: currentCardIndex + 1 });
        }
      },
      
      previousCard: () => {
        const { currentCardIndex } = get();
        if (currentCardIndex > 0) {
          set({ currentCardIndex: currentCardIndex - 1 });
        }
      },
      
      resetProgress: () => set({ 
        currentCardIndex: 0,
        reviewedCount: 0,
        newCount: 0,
        cards: get().cards.map(card => ({ ...card, reviewed: false }))
      }),
    }),
    {
      name: 'cards-storage',
    }
  )
);
