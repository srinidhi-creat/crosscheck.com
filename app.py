import streamlit as st
from question_generator import generate_mcq, voice_questions
from evaluator import mcq_score, speech_score, fake_transcribe
from speech_handler import record_audio

st.set_page_config(page_title="AI Communication Test", layout="centered")

st.title("🧠 AI Communication Test")

# ---------------- STATE ----------------
if "stage" not in st.session_state:
    st.session_state.stage = "mcq"
    st.session_state.answers = []
    st.session_state.voice_scores = []

# ---------------- MCQ ----------------
if st.session_state.stage == "mcq":
    st.header("Step 1: MCQ Test")

    # generate only once
    if "questions" not in st.session_state:
        st.session_state.questions = generate_mcq()

    questions = st.session_state.questions
    correct = []

    st.session_state.answers = []

    for i, (q, opts, c) in enumerate(questions):
        ans = st.radio(
            f"{i+1}. {q}",
            opts,
            key=f"mcq_{i}",
            index=None  # no default selection
        )

        if ans is not None:
            st.session_state.answers.append(opts.index(ans))
        else:
            st.session_state.answers.append(-1)

        correct.append(c)

    if st.button("Submit MCQ"):
        st.session_state.mcq_score = mcq_score(st.session_state.answers, correct)
        st.session_state.stage = "voice"
        st.session_state.voice_index = 0
        st.rerun()

# ---------------- VOICE ----------------
elif st.session_state.stage == "voice":
    st.header("Step 2: Voice Test 🎤")
    st.info("🎤 Click START → Speak → Click NEXT")

    qs = voice_questions()

    # current question index
    i = st.session_state.voice_index

    # stop after 5 questions
    if i >= 5:
        st.session_state.stage = "result"
        st.rerun()

    q = qs[i]

    st.subheader(f"Question {i+1}")
    st.write(q)

    # SINGLE MIC (important)
    audio = record_audio("main_speech")

    if st.button("Next"):
        if audio and len(audio) > 0:
            text = fake_transcribe(audio)
            st.write("📝 Transcribed:", text)

            score = speech_score(text)
            st.session_state.voice_scores.append(score)

            # move to next question
            st.session_state.voice_index += 1
            st.rerun()
        else:
            st.warning("⚠️ Speak first before clicking Next")

# ---------------- RESULT ----------------
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