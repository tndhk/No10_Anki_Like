# app/services/tts_service.py
import os
import uuid
from google.cloud import texttospeech
import asyncio
import os.path

# 音声ファイルの保存ディレクトリ
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "../static/audio")
# ディレクトリが存在しない場合は作成
os.makedirs(AUDIO_DIR, exist_ok=True)

async def generate_audio(text: str) -> str:
    """
    テキストから音声ファイルを生成し、ファイルパスを返す
    
    Args:
        text: 音声に変換するテキスト
        
    Returns:
        生成された音声ファイルのURL
    """
    try:
        # ファイル名を生成（一意なIDを含める）
        file_name = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(AUDIO_DIR, file_name)
        
        # 既に生成済みのファイルがあれば再利用
        if os.path.exists(file_path):
            return f"/static/audio/{file_name}"
        
        # 非同期で音声生成を実行
        await asyncio.to_thread(_generate_tts, text, file_path)
        
        # 相対URLを返す
        return f"/static/audio/{file_name}"
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return ""

def _generate_tts(text: str, output_path: str):
    """
    Google Cloud TTSを使用して音声を生成する実装
    
    Args:
        text: 音声に変換するテキスト
        output_path: 出力ファイルのパス
    """
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    # 音声の設定
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    
    # 音声ファイルの設定
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    # 音声の生成
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    # 音声ファイルとして保存
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
