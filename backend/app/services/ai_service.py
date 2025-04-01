# app/services/ai_service.py
import os
import openai
import uuid
from typing import List, Dict, Any

# OpenAI APIキーを環境変数から取得
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        
        JSON形式で返してください。
        """
        
        # OpenAI APIを呼び出し
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates business English phrase cards for Japanese learners."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        # レスポンスからカード情報を抽出
        content = response.choices[0].message.content
        
        # 取得したJSONをパース
        import json
        try:
            card_data = json.loads(content)
            
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
            
            return cards
        except json.JSONDecodeError:
            # JSONパースに失敗した場合、テキストを解析して構造化
            import re
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
