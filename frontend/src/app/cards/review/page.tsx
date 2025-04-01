// src/app/cards/review/page.tsx
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import CardDetail from '@/components/CardDetail';
import { useCardsStore } from '@/app/store/cards';

export default function ReviewPage() {
  const router = useRouter();
  const { cards, resetProgress } = useCardsStore();

  // カードがない場合はホームに戻る
  useEffect(() => {
    if (cards.length === 0) {
      router.push('/');
    }
  }, [cards.length, router]);

  // 復習を開始する前にカードをリセット
  useEffect(() => {
    resetProgress();
  }, [resetProgress]);

  if (cards.length === 0) {
    return <div className="text-center p-8">カードを読み込み中...</div>;
  }

  return (
    <main className="min-h-screen p-4 bg-gray-50">
      <div className="max-w-md mx-auto">
        <h1 className="text-2xl font-bold mb-6 text-center">復習モード</h1>
        <CardDetail reviewMode={true} />
      </div>
    </main>
  );
}
