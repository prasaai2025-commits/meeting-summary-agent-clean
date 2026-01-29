import os
import subprocess
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHUNK_SECONDS = 300  # 5 minutes

def extract_audio(video_path: str) -> str:
    audio_path = video_path.rsplit(".", 1)[0] + ".wav"
    if os.path.exists(audio_path):
        return audio_path

    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path, "-ar", "16000", "-ac", "1", audio_path],
        check=True
    )
    return audio_path


def split_audio(audio_path: str):
    chunks_dir = audio_path + "_chunks"
    os.makedirs(chunks_dir, exist_ok=True)

    chunk_files = []
    i = 0

    while True:
        out = os.path.join(chunks_dir, f"chunk_{i}.wav")
        cmd = [
            "ffmpeg", "-y",
            "-i", audio_path,
            "-ss", str(i * CHUNK_SECONDS),
            "-t", str(CHUNK_SECONDS),
            out
        ]
        subprocess.run(cmd, stderr=subprocess.DEVNULL)

        if not os.path.exists(out) or os.path.getsize(out) < 1000:
            break

        chunk_files.append(out)
        i += 1

    return chunk_files


def transcribe_audio(file_path: str) -> str:
    if file_path.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".webm")):
        file_path = extract_audio(file_path)

    chunks = split_audio(file_path)

    full_text = []
    for idx, chunk in enumerate(chunks):
        with open(chunk, "rb") as f:
            text = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=f,
                response_format="text"
            )
        full_text.append(text)

    return "\n".join(full_text)
