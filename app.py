import streamlit as st
from question_generator import generate_mcq, voice_questions
from evaluator import mcq_score, speech_score, transcribe_audio
from speech_handler import record_audio, clear_audio

st.set_page_config(page_title="AI Communication Test", layout="centered")
st.title(" AI Communication Test")

# ---------------- STATE ----------------
if "stage" not in st.session_state:
    st.session_state.stage = "mcq"
    st.session_state.answers = []
    st.session_state.voice_scores = []

# ---------------- MCQ ----------------
if st.session_state.stage == "mcq":
    st.header("Step 1: MCQ Test")

    if "questions" not in st.session_state:
        st.session_state.questions = generate_mcq()

    questions = st.session_state.questions
    correct = []
    st.session_state.answers = []

    for i, (q, opts, c) in enumerate(questions):
        ans = st.radio(f"{i+1}. {q}", opts, key=f"mcq_{i}", index=None)
        st.session_state.answers.append(opts.index(ans) if ans is not None else -1)
        correct.append(c)

    if st.button("Submit MCQ"):
        st.session_state.mcq_score = mcq_score(st.session_state.answers, correct)
        st.session_state.stage = "voice"
        st.session_state.voice_index = 0
        st.rerun()

# ---------------- VOICE ----------------
elif st.session_state.stage == "voice":
    st.header("Step 2: Voice Test ")

    qs = voice_questions()
    i = st.session_state.voice_index

    if i >= 5:
        st.session_state.stage = "result"
        st.rerun()

    st.progress(i / 5, text=f"Question {i+1} of 5")
    st.subheader(qs[i])
    st.info(" Click the microphone below to record, then click **Next** when done.")

    audio_key = f"speech_{i}"
    audio = record_audio(audio_key)

    # Show status
    if audio is not None:
        st.success(" Recording captured! Click **Next ▶** to continue.")
        st.audio(audio)  # playback so user can verify
    else:
        st.caption("No recording yet — press the mic button above.")

    if st.button("Next ▶", key=f"next_{i}"):
        if audio is not None:
            raw_bytes = audio.read() if hasattr(audio, "read") else audio
            text = transcribe_audio(raw_bytes)
            st.write(" Transcribed:", text)
            st.session_state.voice_scores.append(speech_score(text))
            clear_audio(audio_key)
            st.session_state.voice_index += 1
            st.rerun()
        else:
            st.warning(" Please record an answer before clicking Next.")

# ---------------- RESULT ----------------
elif st.session_state.stage == "result":
    st.header("Final Results")
    st.subheader(f"MCQ Score: {st.session_state.get('mcq_score', 0)} / 30")

    scores = st.session_state.voice_scores
    if scores:
        g = sum(s[0] for s in scores) / len(scores)
        c = sum(s[1] for s in scores) / len(scores)
        sp = sum(s[2] for s in scores) / len(scores)

        def color(x):
            return "green" if x > 7 else "orange" if x > 4 else "red"

        st.markdown(f"<h3 style='color:{color(g)}'>Grammar: {round(g,2)} / 10</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{color(c)}'>Confidence: {round(c,2)} / 10</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{color(sp)}'>Speed: {round(sp,2)} / 10</h3>", unsafe_allow_html=True)
    else:
        st.warning("No voice scores recorded.")

    if st.button("Restart"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
