// src/components/CardList.tsx
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useCardsStore } from '@/app/store/cards';
import Link from 'next/link';

const CardList = () => {
  const router = useRouter();
  const { cards, setCards } = useCardsStore();

  useEffect(() => {
    // ローカルストレージからカードを取得、なければAPIから取得
    const fetchCards = async () => {
      if (cards.length === 0) {
        try {
          // この時点でカードはすでに生成されていると想定
          const response = await fetch('/api/cards');
          if (response.ok) {
            const data = await response.json();
            setCards(data.cards);
          } else {
            // カードがない場合はホームに戻る
            router.push('/');
          }
        } catch (error) {
          console.error('Error fetching cards:', error);
          router.push('/');
        }
      }
    };

    fetchCards();
  }, [cards.length, router, setCards]);

  const handleStartReview = () => {
    router.push('/cards/review');
  };

  if (cards.length === 0) {
    return <div className="text-center p-8">カードを読み込み中...</div>;
  }

  return (
    <div className="card-list max-w-md mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6 text-center">Generated Cards</h2>
      <ul className="space-y-2 mb-6">
        {cards.map((card) => (
          <li 
            key={card.id}
            className="p-4 border border-gray-200 rounded-md hover:bg-gray-50 transition-colors"
          >
            <Link href={`/cards/${card.id}`}>
              <div className="text-lg font-medium">{card.phrase}</div>
              <div className="text-sm text-gray-500">{card.situation}</div>
            </Link>
          </li>
        ))}
      </ul>
      <button
        onClick={handleStartReview}
        className="w-full bg-blue-600 text-white p-3 rounded-md hover:bg-blue-700 transition-colors"
      >
        復習する
      </button>
    </div>
  );
};

export default CardList;
