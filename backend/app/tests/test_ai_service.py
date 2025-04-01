# app/tests/test_ai_service.py
import pytest
from unittest.mock import patch, MagicMock
import json
from services.ai_service import generate_cards

# OpenAIのモックレスポンス
MOCK_OPENAI_RESPONSE = {
    "choices": [
        {
            "message": {
                "content": json.dumps([
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
                ])
            }
        }
    ]
}

def test_generate_cards_success():
    """カード生成が成功するケースのテスト"""
    with patch('openai.ChatCompletion.create') as mock_create:
        # OpenAI APIのモックを設定
        mock_create.return_value = MagicMock(**MOCK_OPENAI_RESPONSE)
        
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
    with patch('openai.ChatCompletion.create') as mock_create:
        # エラーを発生させる
        mock_create.side_effect = Exception("API Error")
        
        # エラーがraiseされることを確認
        with pytest.raises(Exception) as excinfo:
            generate_cards("meeting expressions")
        
        assert "API Error" in str(excinfo.value)

def test_generate_cards_text_parsing():
    """JSONではなくテキスト形式で返ってきた場合のパースをテスト"""
    with patch('openai.ChatCompletion.create') as mock_create:
        # テキスト形式のレスポンス
        text_response = {
            "choices": [
                {
                    "message": {
                        "content": """
1. Phrase: Let's touch base next week.
   Example: I'll be out of office until Monday, so let's touch base next week to discuss the project progress.
   Translation: 来週また連絡を取りましょう。
   Situation: 後日のフォローアップを提案する時

2. Phrase: Could you elaborate on that?
   Example: That's an interesting proposal. Could you elaborate on that a bit more?
   Translation: もう少し詳しく説明していただけますか？
   Situation: 会議やプレゼンで詳細を求める時
                        """
                    }
                }
            ]
        }
        mock_create.return_value = MagicMock(**text_response)
        
        # カード生成を実行
        result = generate_cards("meeting expressions", count=2)
        
        # 結果の検証
        assert len(result) == 2
        assert "id" in result[0]
        assert result[0]["phrase"] == "Let's touch base next week."
