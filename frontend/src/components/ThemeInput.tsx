// src/components/ThemeInput.tsx
import { useState } from 'react';
import { useRouter } from 'next/navigation';

const ThemeInput = () => {
  const [theme, setTheme] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!theme.trim()) return;

    try {
      setLoading(true);
      // APIエンドポイントを呼び出す
      const response = await fetch('/api/generate-cards', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ theme }),
      });

      if (!response.ok) {
        throw new Error('カードの生成に失敗しました');
      }

      const data = await response.json();
      
      // カード一覧画面に遷移
      router.push('/cards');
    } catch (error) {
      console.error('Error:', error);
      alert('カードの生成中にエラーが発生しました。もう一度お試しください。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="theme-page max-w-md mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6 text-center">今日の学習テーマは？</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
          placeholder="例: 会議で使う表現"
          className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-3 rounded-md hover:bg-blue-700 transition-colors disabled:bg-blue-300"
          disabled={loading}
        >
          {loading ? '生成中...' : 'AIカード自動生成'}
        </button>
      </form>
    </div>
  );
};

export default ThemeInput;
