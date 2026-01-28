import os
import subprocess
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_audio(video_path: str) -> str:
    audio_path = video_path.rsplit(".", 1)[0] + ".wav"

    if os.path.exists(audio_path):
        return audio_path

    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path, "-ar", "16000", "-ac", "1", audio_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return audio_path


def transcribe_audio(file_path: str) -> str:
    # If video, convert to audio first
    if file_path.lower().endswith((".mp4", ".mkv", ".avi", ".mov")):
        file_path = extract_audio(file_path)

    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio_file
        )

    return transcript.text
