import streamlit as st
from question_generator import generate_mcq, voice_questions
from evaluator import mcq_score, speech_score, fake_transcribe
from speech_handler import record_audio

st.set_page_config(page_title="AI Communication Test", layout="centered")

st.title("🧠 AI Communication Test")


if "stage" not in st.session_state:
    st.session_state.stage = "mcq"
    st.session_state.answers = []
    st.session_state.voice_scores = []


if st.session_state.stage == "mcq":
    st.header("Step 1: MCQ Test")

    questions = generate_mcq()
    correct = []

    
    st.session_state.answers = []

    for i, (q, opts, c) in enumerate(questions):
        ans = st.radio(f"{i+1}. {q}", opts, key=f"mcq_{i}")
        st.session_state.answers.append(opts.index(ans))
        correct.append(c)

    if st.button("Submit MCQ"):
        st.session_state.mcq_score = mcq_score(st.session_state.answers, correct)
        st.session_state.stage = "voice"
        st.rerun()


elif st.session_state.stage == "voice":
    st.header("Step 2: Voice Test 🎤")
    st.info("🎤 Using real mic input via browser")

    qs = voice_questions()

    for i, q in enumerate(qs[:5]):
        st.subheader(f"Question {i+1}")
        st.write(q)

        
        audio = record_audio(f"speech_{i}")

        if st.button(f"Analyze Answer {i+1}", key=f"btn_{i}"):
            if audio:
                text = fake_transcribe(audio)
                st.write("📝 Transcribed:", text)

                score = speech_score(text)
                st.session_state.voice_scores.append(score)
            else:
                st.warning("⚠️ No audio detected. Click mic and speak first.")

        st.divider()

    if st.button("Finish Test"):
        if len(st.session_state.voice_scores) == 0:
            st.warning("⚠️ Please answer at least one question")
        else:
            st.session_state.stage = "result"
            st.rerun()


elif st.session_state.stage == "result":
    st.header("Final Results")

    st.subheader(f"MCQ Score: {st.session_state.mcq_score}/30")

    g = sum([s[0] for s in st.session_state.voice_scores]) / len(st.session_state.voice_scores)
    c = sum([s[1] for s in st.session_state.voice_scores]) / len(st.session_state.voice_scores)
    s = sum([s[2] for s in st.session_state.voice_scores]) / len(st.session_state.voice_scores)

    def color(x):
        return "green" if x > 7 else "orange" if x > 4 else "red"

    st.markdown(f"<h3 style='color:{color(g)}'>Grammar: {round(g,2)}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{color(c)}'>Confidence: {round(c,2)}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{color(s)}'>Speed: {round(s,2)}</h3>", unsafe_allow_html=True)