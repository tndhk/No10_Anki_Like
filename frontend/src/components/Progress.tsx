// src/components/Progress.tsx
'use client';

import { useCardsStore } from '@/app/store/cards';
import { useRouter } from 'next/navigation';

const Progress = () => {
  const router = useRouter();
  const { reviewedCount, newCount, cards } = useCardsStore();
  
  const totalCards = cards.length;
  const progressPercentage = totalCards > 0 
    ? Math.round((reviewedCount / totalCards) * 100) 
    : 0;

  const getMessage = () => {
    if (progressPercentage === 100) {
      return "完璧です！全てのカードを復習しました！";
    } else if (progressPercentage >= 75) {
      return "すごい進捗です！あと少しです！";
    } else if (progressPercentage >= 50) {
      return "良い調子です！半分以上完了しました！";
    } else if (progressPercentage >= 25) {
      return "良いスタートです！続けましょう！";
    } else {
      return "今日のレッスンを始めましょう！";
    }
  };

  return (
    <div className="progress-page max-w-md mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6 text-center">今日の進捗</h2>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="mb-4">
          <div className="text-sm text-gray-600 mb-1">全体の進捗</div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div 
              className="bg-blue-600 h-4 rounded-full" 
              style={{ width: `${progressPercentage}%` }}
            ></div>
          </div>
          <div className="text-right text-sm text-gray-600 mt-1">
            {progressPercentage}%
          </div>
        </div>
        
        <p className="mb-2 text-lg">・復習したカード：{reviewedCount}枚</p>
        <p className="mb-4 text-lg">・新しく覚えたカード：{newCount}枚</p>
        
        <p className="text-center font-medium text-lg text-blue-700">
          {getMessage()}
        </p>
      </div>
      
      <div className="flex space-x-2">
        <button
          onClick={() => router.push('/cards')}
          className="flex-1 bg-gray-500 text-white p-3 rounded-md hover:bg-gray-600 transition-colors"
        >
          カード一覧に戻る
        </button>
        
        <button
          onClick={() => router.push('/')}
          className="flex-1 bg-blue-600 text-white p-3 rounded-md hover:bg-blue-700 transition-colors"
        >
          新しいテーマで学習
        </button>
      </div>
    </div>
  );
};

export default Progress;
