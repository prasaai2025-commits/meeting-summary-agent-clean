
import speech_recognition as sr

def transcribe_audio(file_path: str) -> str:
    r = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
    except Exception as e:
        text = "Transcription failed: " + str(e)

    return text
