# app/services/ai_service.py
import os
import uuid
import json
import re
from typing import List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数のロード
load_dotenv()

# Google Gemini API設定
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash")  # デフォルト値を設定

def generate_cards(theme: str, count: int = 5) -> List[Dict[str, Any]]:
    """
    指定されたテーマに基づいてビジネス英語カードを生成する
    
    Args:
        theme: 学習テーマ
        count: 生成するカードの数
        
    Returns:
        生成されたカードのリスト
    """
    try:
        # APIリクエストのプロンプト
        prompt = f"""
        以下の条件に基づいてビジネス英語のフレーズカードを{count}枚生成してください。
        テーマ: {theme}
        
        各カードには以下の情報を含めてください:
        1. phrase: ビジネスで実際に使われる英語フレーズ
        2. example: フレーズを使った例文
        3. translation: 日本語訳
        4. situation: このフレーズが使われるビジネスシチュエーション（日本語）
        
        JSON形式で返してください。以下の形式で返答してください:
        [
          {{
            "phrase": "フレーズ1",
            "example": "例文1",
            "translation": "翻訳1",
            "situation": "状況1"
          }},
          {{
            "phrase": "フレーズ2",
            "example": "例文2",
            "translation": "翻訳2",
            "situation": "状況2"
          }}
        ]
        
        有効なJSONのみを返してください。余計な説明は不要です。
        """
        
        # Gemini モデルを選択
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Gemini APIを呼び出し
        response = model.generate_content(prompt)
        
        # レスポンスからカード情報を抽出
        content = response.text
        
        # JSONを検出して抽出するヘルパー関数
        def extract_json_from_text(text):
            # JSONブロックを検出（```jsonや```の間のテキストも対応）
            json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
            match = re.search(json_pattern, text)
            if match:
                return match.group(1)
            
            # JSONブロックがなければ、テキスト全体をJSONとして解釈
            return text
        
        # JSONテキストを抽出
        json_content = extract_json_from_text(content)
        
        # 取得したJSONをパース
        try:
            card_data = json.loads(json_content)
            
            # レスポンスの形式が異なる場合に対応
            if isinstance(card_data, dict) and "cards" in card_data:
                cards = card_data["cards"]
            elif isinstance(card_data, list):
                cards = card_data
            else:
                cards = [card_data]
                
            # 各カードにIDを追加
            for card in cards:
                card["id"] = str(uuid.uuid4())
            
            return cards[:count]  # 指定された数のカードを返す
            
        except json.JSONDecodeError:
            # JSONパースに失敗した場合、テキストを解析して構造化
            cards = []
            
            # カードを分割するパターンを探す
            card_texts = re.split(r'\n\s*\d+\.\s*', content)
            if len(card_texts) <= 1:
                card_texts = content.split("\n\n")
            
            for i, card_text in enumerate(card_texts):
                if not card_text.strip():
                    continue
                    
                card = {
                    "id": str(uuid.uuid4()),
                    "phrase": "",
                    "example": "",
                    "translation": "",
                    "situation": ""
                }
                
                # 各行からデータを抽出
                lines = card_text.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith("Phrase:") or line.startswith("phrase:"):
                        card["phrase"] = line.split(":", 1)[1].strip()
                    elif line.startswith("Example:") or line.startswith("example:"):
                        card["example"] = line.split(":", 1)[1].strip()
                    elif line.startswith("Translation:") or line.startswith("translation:"):
                        card["translation"] = line.split(":", 1)[1].strip()
                    elif line.startswith("Situation:") or line.startswith("situation:"):
                        card["situation"] = line.split(":", 1)[1].strip()
                
                if card["phrase"]:  # 最低限フレーズがあるカードのみ追加
                    cards.append(card)
            
            return cards[:count]  # 指定数だけ返す
            
    except Exception as e:
        print(f"Error generating cards: {str(e)}")
        raise e
