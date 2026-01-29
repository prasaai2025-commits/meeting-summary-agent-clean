from app.transcribe import transcribe_audio
from app.summarize import summarize_text
from app.utils import save_docx, save_pdf

def run_agent(path, job_id):
    try:
        with open(f"status/{job_id}.txt", "w") as f:
            f.write("transcribing")

        text = transcribe_audio(path)

        with open(f"status/{job_id}.txt", "w") as f:
            f.write("summarizing")

        summary = summarize_text(text)

        save_docx(summary, f"outputs/{job_id}.docx")
        save_pdf(summary, f"outputs/{job_id}.pdf")

        with open(f"status/{job_id}.txt", "w") as f:
            f.write("completed")

    except Exception as e:
        with open(f"status/{job_id}.txt", "w") as f:
            f.write(f"error: {e}")
