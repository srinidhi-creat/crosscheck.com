import fitz  # PyMuPDF

SKILLS = [
    "python", "java", "c++", "machine learning",
    "data science", "react", "node", "sql",
    "deep learning", "nlp"
]

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(text):
    text = text.lower()
    found_skills = []
    
    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)
    
    return found_skills