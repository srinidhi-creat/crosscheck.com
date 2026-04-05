import streamlit as st
import fitz
from naive_bayes_scorer import train_and_score

def extract_text_from_stream(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    return " ".join([page.get_text() for page in doc])

st.set_page_config(page_title="cv matcher", layout="centered")
st.title("naive bayes cv/jd matcher")

cv_file = st.file_uploader("upload candidate cv (pdf)", type=["pdf"])
jd_text = st.text_area("paste job description", height=200)

if st.button("score candidate"):
    if cv_file and jd_text:
        with st.spinner("training model and scoring..."):
            cv_text = extract_text_from_stream(cv_file)
            
            # call the function from the file you just made
            score, sentences, probs = train_and_score(cv_text, jd_text)
            
            st.metric(label="match score", value=f"{score}/100")
            st.progress(score / 100.0)
            
            st.subheader("how the model saw it")
            st.write("here are the most relevant sentences found in the cv based on our dynamic tf-idf naive bayes classifier:")
            
            # show the top 3 highest scoring sentences to prove it works
            sentence_scores = list(zip(sentences, probs))
            sentence_scores.sort(key=lambda x: x[1], reverse=True)
            
            for sent, prob in sentence_scores[:3]:
                if prob > 0.5:
                    st.success(f"{sent} (relevance: {prob:.2f})")
    else:
        st.error("upload a pdf and paste a jd first.")