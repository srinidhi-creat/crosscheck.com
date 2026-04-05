import random

grammar = [
    ("Choose correct sentence:", ["She go", "She goes", "She going", "She gone"], 1),
    ("He ___ playing", ["is", "are", "am", "be"], 0),
]

verbal = [
    ("Professional greeting?", ["Yo", "Hey bro", "Good morning", "Sup"], 2),
]

terms = [
    ("JD means?", ["Job Description", "Job Data", "Joint Dev", "None"], 0),
]

def generate_mcq():
    def expand(q, n):
        return random.sample(q * 10, n)

    questions = []
    questions += expand(grammar, 10)
    questions += expand(verbal, 10)
    questions += expand(terms, 10)

    random.shuffle(questions)
    return questions


def voice_questions():
    base = [
        "Tell me about yourself",
        "Why should we hire you?",
        "What are your strengths?",
        "Describe a failure"
    ]
    return base * 8