import os
import subprocess
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_audio(video_path: str) -> str:
    audio_path = video_path.rsplit(".", 1)[0] + ".wav"

    if os.path.exists(audio_path):
        return audio_path

    # Convert video to 16kHz mono wav (best for Whisper)
    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path, "-ar", "16000", "-ac", "1", audio_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

    return audio_path


def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio/video using OpenAI Whisper API (FAST).
    """

    # If video → extract audio first
    if file_path.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".webm")):
        file_path = extract_audio(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio_file,
            response_format="text"
        )

    return response
