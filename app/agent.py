from app.transcribe import transcribe_audio
from app.summarize import summarize_text

def run_agent(path, job_id):
    text = transcribe_audio(path)

    # Stage 1: compress transcript
    compressed = summarize_text(text, mode="compress")

    # Stage 2: professional summary
    final = summarize_text(compressed, mode="final")

    return final
