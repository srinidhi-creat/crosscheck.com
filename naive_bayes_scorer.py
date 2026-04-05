import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    return " ".join([page.get_text() for page in doc])

def train_and_score(cv_text, jd_text):
    # 1. prep the data. 
    # we're going to "train" the model on the JD.
    # we split the JD into sentences. these are our "positive" examples.
    jd_sentences = [s.strip() for s in jd_text.split('.') if len(s.strip()) > 10]
    
    # we need "negative" examples. in a real scenario, you'd have a dataset of bad resumes.
    # for a hackathon, we generate dummy negative data or use generic filler text.
    negative_sentences = [
        "i like to walk my dog.", "proficient in microsoft word.", 
        "managed a team of zero.", "looking for a job to pay rent.",
        "i am a hard worker.", "excellent communication skills."
    ]
    
    # combine training data
    X_train = jd_sentences + negative_sentences
    # labels: 1 for JD (relevant), 0 for negative (irrelevant)
    y_train = [1] * len(jd_sentences) + [0] * len(negative_sentences)
    
    # 2. vectorize the text (turn words into numbers)
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    
    # 3. train the naive bayes classifier
    clf = MultinomialNB()
    clf.fit(X_train_vec, y_train)
    
    # 4. score the CV
    cv_sentences = [s.strip() for s in cv_text.split('.') if len(s.strip()) > 10]
    if not cv_sentences:
        return 0
        
    X_cv_vec = vectorizer.transform(cv_sentences)
    
    # get probabilities of being in class 1 (relevant)
    probs = clf.predict_proba(X_cv_vec)[:, 1]
    
    # 5. calculate final score (0-100)
    # average the probabilities of all sentences in the CV
    avg_prob = np.mean(probs)
    score = int(avg_prob * 100)
    
    return score, cv_sentences, probs

# --- usage ---
# cv_text = extract_text("resume.pdf")
# jd_text = "We need a Python developer with 5 years experience in machine learning. Must know scikit-learn and pandas. Experience with AWS is a plus."
# score, sentences, probabilities = train_and_score(cv_text, jd_text)
# print(f"Score: {score}/100")