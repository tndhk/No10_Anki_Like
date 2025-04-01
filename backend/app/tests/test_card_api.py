# backend/app/tests/test_card_api.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from services.ai_service import generate_cards
from services.tts_service import generate_audio

client = TestClient(app)

# AIサービスとTTSサービスのモック
@pytest.fixture
def mock_services():
    with patch('api.cards.generate_cards') as mock_generate_cards, \
         patch('api.cards.generate_audio') as mock_generate_audio:
        
        # AIサービスのレスポンスをモック
        mock_generate_cards.return_value = [
            {
                "id": "test-id-1",
                "phrase": "Let's touch base next week.",
                "example": "I'll be out of office until Monday, so let's touch base next week.",
                "translation": "来週また連絡を取りましょう。",
                "situation": "後日のフォローアップを提案する時"
            }
        ]
        
        # TTSサービスのレスポンスをモック
        mock_generate_audio.return_value = "/static/audio/test-audio.mp3"
        
        yield

def test_generate_cards_api(mock_services):
    """カード生成APIが正常に動作するか確認するテスト"""
    # リクエスト送信
    response = client.post(
        "/api/generate-cards",
        json={"theme": "meeting expressions"}
    )
    
    # ステータスコード確認
    assert response.status_code == 200
    
    # レスポンス内容確認
    data = response.json()
    assert "cards" in data
    assert len(data["cards"]) == 1
    assert data["cards"][0]["phrase"] == "Let's touch base next week."
    assert data["cards"][0]["audio_url"] == "/static/audio/test-audio.mp3"

def test_generate_cards_api_empty_theme():
    """空のテーマでリクエストした場合のテスト"""
    # 空のテーマでリクエスト
    response = client.post(
        "/api/generate-cards",
        json={"theme": ""}
    )
    
    # 400エラーが返ることを確認
    assert response.status_code == 400
    assert "Theme cannot be empty" in response.json()["detail"]

def test_generate_cards_api_service_error(mock_services):
    """サービスでエラーが発生した場合のテスト"""
    # AIサービスで例外発生をモック
    with patch('api.cards.generate_cards', side_effect=Exception("Service error")):
        response = client.post(
            "/api/generate-cards",
            json={"theme": "meeting expressions"}
        )
        
        # 500エラーが返ることを確認
        assert response.status_code == 500
        assert "Service error" in response.json()["detail"]