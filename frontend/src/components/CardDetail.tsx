// src/components/CardDetail.tsx
'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Card } from '@/types/card';
import { useCardsStore } from '@/app/store/cards';

interface CardDetailProps {
  cardId?: string;
  reviewMode?: boolean;
}

const CardDetail = ({ cardId, reviewMode = false }: CardDetailProps) => {
  const router = useRouter();
  const audioRef = useRef<HTMLAudioElement>(null);
  const [loading, setLoading] = useState(false);
  
  const { 
    cards, 
    currentCardIndex, 
    markAsReviewed, 
    nextCard, 
    previousCard 
  } = useCardsStore();

  // カードの取得
  const card: Card | undefined = cardId 
    ? cards.find(c => c.id === cardId) 
    : cards[currentCardIndex];

  // 音声を再生
  const playAudio = () => {
    if (audioRef.current && card?.audio_url) {
      audioRef.current.play();
    }
  };

  // カードがマークされたときの処理
  const handleCardMarked = (reviewAgain: boolean) => {
    if (!card) return;
    
    // カードをレビュー済みとしてマーク
    if (!reviewAgain) {
      markAsReviewed(card.id);
    }
    
    // レビューモードの場合、次のカードへ
    if (reviewMode) {
      if (currentCardIndex < cards.length - 1) {
        nextCard();
      } else {
        // 全カード終了、進捗画面へ
        router.push('/progress');
      }
    }
  };

  // カードが存在しない場合
  if (!card) {
    return <div className="text-center p-8">カードが見つかりません</div>;
  }

  return (
    <div className="card-detail max-w-md mx-auto p-6">
      {reviewMode && (
        <h2 className="text-xl font-bold mb-4 text-center">
          Card {currentCardIndex + 1}/{cards.length}
        </h2>
      )}
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <p className="mb-4">
          <strong className="block text-gray-600 text-sm">Phrase:</strong>
          <span className="text-xl font-medium">{card.phrase}</span>
        </p>
        
        <p className="mb-4">
          <strong className="block text-gray-600 text-sm">Example:</strong>
          <span>{card.example}</span>
        </p>
        
        <p className="mb-4">
          <strong className="block text-gray-600 text-sm">Japanese:</strong>
          <span>{card.translation}</span>
        </p>
        
        <p className="mb-6">
          <strong className="block text-gray-600 text-sm">Scene:</strong>
          <span>{card.situation}</span>
        </p>
        
        {card.audio_url && (
          <>
            <button
              onClick={playAudio}
              className="w-full bg-gray-200 text-gray-800 p-2 rounded-md hover:bg-gray-300 transition-colors mb-4"
              disabled={loading}
            >
              ▶︎ 音声再生
            </button>
            <audio ref={audioRef} src={card.audio_url} />
          </>
        )}
      </div>
      
      {reviewMode ? (
        <div className="flex space-x-2">
          <button
            onClick={() => handleCardMarked(true)}
            className="flex-1 bg-yellow-500 text-white p-3 rounded-md hover:bg-yellow-600 transition-colors"
          >
            もう一度
          </button>
          <button
            onClick={() => handleCardMarked(false)}
            className="flex-1 bg-green-600 text-white p-3 rounded-md hover:bg-green-700 transition-colors"
          >
            OK
          </button>
        </div>
      ) : (
        <div className="flex space-x-2">
          <button
            onClick={() => router.back()}
            className="flex-1 bg-gray-500 text-white p-3 rounded-md hover:bg-gray-600 transition-colors"
          >
            戻る
          </button>
          {!card.reviewed && (
            <button
              onClick={() => {
                markAsReviewed(card.id);
                router.back();
              }}
              className="flex-1 bg-green-600 text-white p-3 rounded-md hover:bg-green-700 transition-colors"
            >
              覚えた
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default CardDetail;
