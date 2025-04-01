# app/tests/test_ai_service.py
import pytest
from unittest.mock import patch, MagicMock
import json
from services.ai_service import generate_cards

# Gemini APIのモックレスポンスクラス
class MockGeminiResponse:
    def __init__(self, text):
        self.text = text

# モックレスポンス用のJSON
MOCK_GEMINI_RESPONSE_JSON = """
[
  {
    "phrase": "Let's touch base next week.",
    "example": "I'll be out of office until Monday, so let's touch base next week to discuss the project progress.",
    "translation": "来週また連絡を取りましょう。",
    "situation": "後日のフォローアップを提案する時"
  },
  {
    "phrase": "Could you elaborate on that?",
    "example": "That's an interesting proposal. Could you elaborate on that a bit more?",
    "translation": "もう少し詳しく説明していただけますか？",
    "situation": "会議やプレゼンで詳細を求める時"
  }
]
"""

# モックレスポンス用のテキスト（JSON形式ではない）
MOCK_GEMINI_RESPONSE_TEXT = """
1. Phrase: Let's touch base next week.
   Example: I'll be out of office until Monday, so let's touch base next week to discuss the project progress.
   Translation: 来週また連絡を取りましょう。
   Situation: 後日のフォローアップを提案する時

2. Phrase: Could you elaborate on that?
   Example: That's an interesting proposal. Could you elaborate on that a bit more?
   Translation: もう少し詳しく説明していただけますか？
   Situation: 会議やプレゼンで詳細を求める時
"""

def test_generate_cards_success():
    """カード生成が成功するケースのテスト"""
    with patch('google.generativeai.GenerativeModel') as mock_model_class:
        # モックモデルと応答を設定
        mock_model = MagicMock()
        mock_model.generate_content.return_value = MockGeminiResponse(MOCK_GEMINI_RESPONSE_JSON)
        mock_model_class.return_value = mock_model
        
        # カード生成を実行
        result = generate_cards("meeting expressions", count=2)
        
        # 結果の検証
        assert len(result) == 2
        assert "id" in result[0]
        assert result[0]["phrase"] == "Let's touch base next week."
        assert result[1]["phrase"] == "Could you elaborate on that?"
        assert result[0]["situation"] == "後日のフォローアップを提案する時"

def test_generate_cards_error_handling():
    """APIエラー時のハンドリングテスト"""
    with patch('google.generativeai.GenerativeModel') as mock_model_class:
        # モックモデルを設定してエラーを発生させる
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_model_class.return_value = mock_model
        
        # エラーがraiseされることを確認
        with pytest.raises(Exception) as excinfo:
            generate_cards("meeting expressions")
        
        assert "API Error" in str(excinfo.value)

def test_generate_cards_text_parsing():
    """JSONではなくテキスト形式で返ってきた場合のパースをテスト"""
    with patch('google.generativeai.GenerativeModel') as mock_model_class:
        # モックモデルと応答を設定
        mock_model = MagicMock()
        mock_model.generate_content.return_value = MockGeminiResponse(MOCK_GEMINI_RESPONSE_TEXT)
        mock_model_class.return_value = mock_model
        
        # カード生成を実行
        result = generate_cards("meeting expressions", count=2)
        
        # 結果の検証
        assert len(result) == 2
        assert "id" in result[0]
        assert result[0]["phrase"] == "Let's touch base next week."
