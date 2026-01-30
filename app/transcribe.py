
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(path: str) -> str:
    with open(path, "rb") as audio:
        result = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio
        )
    return result.text
