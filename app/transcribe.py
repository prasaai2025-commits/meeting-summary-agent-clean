import whisper
import subprocess
import os

model = whisper.load_model("base")

def extract_audio(video_path: str) -> str:
    audio_path = video_path.rsplit(".", 1)[0] + ".wav"

    if os.path.exists(audio_path):
        return audio_path

    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return audio_path

def transcribe_audio(path: str) -> str:
    if path.lower().endswith((".mp4", ".mkv", ".avi")):
        path = extract_audio(path)

    result = model.transcribe(path)
    return result["text"]
