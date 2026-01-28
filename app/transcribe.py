from faster_whisper import WhisperModel
import subprocess
import os
import math
import uuid

# FAST + LIGHT model (best for Render CPU)
model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

# chunk size = 2 minutes
CHUNK_SECONDS = 120


def extract_audio(video_path: str) -> str:
    audio_path = video_path.rsplit(".", 1)[0] + ".wav"

    if os.path.exists(audio_path):
        return audio_path

    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path, "-ar", "16000", "-ac", "1", audio_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return audio_path


def get_audio_duration(path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration", "-of",
         "default=noprint_wrappers=1:nokey=1", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return float(result.stdout.strip())


def split_audio(path: str):
    duration = get_audio_duration(path)
    chunks = []

    total_chunks = math.ceil(duration / CHUNK_SECONDS)

    for i in range(total_chunks):
        start = i * CHUNK_SECONDS
        out_file = f"/tmp/chunk_{uuid.uuid4().hex}.wav"

        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", path,
                "-ss", str(start),
                "-t", str(CHUNK_SECONDS),
                "-ar", "16000",
                "-ac", "1",
                out_file
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        chunks.append(out_file)

    return chunks


def transcribe_audio(path: str) -> str:
    # convert video to audio if needed
    if path.lower().endswith((".mp4", ".mkv", ".avi", ".mov")):
        path = extract_audio(path)

    chunks = split_audio(path)
    full_text = ""

    for chunk in chunks:
        segments, info = model.transcribe(
            chunk,
            beam_size=1,
            vad_filter=True,
            chunk_length=30,
            language="en"
        )

        for segment in segments:
            full_text += segment.text + " "

        os.remove(chunk)

    return full_text.strip()
