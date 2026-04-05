import textstat


def mcq_score(user, correct):
    return sum(1 for u, c in zip(user, correct) if u == c)


def speech_score(text):
    words = len(text.split())
    grammar = min(10, textstat.flesch_reading_ease(text) / 10)
    confidence = min(10, words / 8)
    speed = min(10, words / 5)
    return grammar, confidence, speed


def transcribe_audio(audio_bytes):
    """
    Transcription stub. Replace this with a real STT call, e.g.:
      - OpenAI Whisper API
      - Google Speech-to-Text
      - local whisper: import whisper; model.transcribe(...)
    For now returns a placeholder so scoring still works.
    """
    if not audio_bytes:
        return ""
    # TODO: replace with real transcription
    return "This is a simulated spoken response demonstrating communication ability"