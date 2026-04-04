import textstat

def mcq_score(user, correct):
    return sum([1 for u, c in zip(user, correct) if u == c])


def speech_score(text):
    words = len(text.split())

    grammar = min(10, textstat.flesch_reading_ease(text) / 10)
    confidence = min(10, words / 8)
    speed = min(10, words / 5)

    return grammar, confidence, speed


def fake_transcribe(audio):
    return "This is a simulated spoken response demonstrating communication ability"