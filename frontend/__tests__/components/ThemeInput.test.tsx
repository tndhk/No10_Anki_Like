// frontend/__tests__/components/ThemeInput.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ThemeInput from '@/components/ThemeInput';
import '@testing-library/jest-dom';

// モックの作成
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

global.fetch = jest.fn();

describe('ThemeInput Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ success: true }),
    });
  });

  test('renders the theme input form', () => {
    render(<ThemeInput />);
    
    // 見出しが表示されるか
    expect(screen.getByText('今日の学習テーマは？')).toBeInTheDocument();
    
    // 入力フィールドが存在するか
    expect(screen.getByPlaceholderText('例: 会議で使う表現')).toBeInTheDocument();
    
    // ボタンが表示されているか
    expect(screen.getByText('AIカード自動生成')).toBeInTheDocument();
  });

  test('handles input change correctly', () => {
    render(<ThemeInput />);
    
    const input = screen.getByPlaceholderText('例: 会議で使う表現');
    fireEvent.change(input, { target: { value: 'プレゼンテーション' } });
    
    expect(input).toHaveValue('プレゼンテーション');
  });

  test('shows error when submitting empty theme', () => {
    render(<ThemeInput />);
    
    // 空のままフォームを送信
    const button = screen.getByText('AIカード自動生成');
    fireEvent.click(button);
    
    // エラーメッセージが表示されるか
    expect(screen.getByText('テーマを入力してください')).toBeInTheDocument();
  });

  test('submits the form and calls the API', async () => {
    render(<ThemeInput />);
    
    // テーマを入力
    const input = screen.getByPlaceholderText('例: 会議で使う表現');
    fireEvent.change(input, { target: { value: 'プレゼンテーション' } });
    
    // フォームを送信
    const button = screen.getByText('AIカード自動生成');
    fireEvent.click(button);
    
    // APIが呼び出されたことを確認
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/generate-cards', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ theme: 'プレゼンテーション' }),
      });
    });
    
    // ローディング状態を確認
    expect(button).toBeDisabled();
    expect(screen.getByText('生成中...')).toBeInTheDocument();
  });

  test('shows error when API call fails', async () => {
    // モックをエラーにオーバーライド
    (global.fetch as jest.Mock).mockRejectedValue(new Error('API Error'));
    
    render(<ThemeInput />);
    
    // テーマを入力してフォームを送信
    const input = screen.getByPlaceholderText('例: 会議で使う表現');
    fireEvent.change(input, { target: { value: 'プレゼンテーション' } });
    
    const button = screen.getByText('AIカード自動生成');
    fireEvent.click(button);
    
    // エラーメッセージが表示されることを確認
    await waitFor(() => {
      expect(screen.getByText('カードの生成中にエラーが発生しました。もう一度お試しください。')).toBeInTheDocument();
    });
  });
});