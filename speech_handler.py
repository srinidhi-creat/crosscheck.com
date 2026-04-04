import streamlit as st


def record_audio(key):
    """
    Uses Streamlit's built-in st.audio_input (available in Streamlit >= 1.32).
    Returns the UploadedFile object (has .read(), .name, .size), or None.
    Falls back to a file uploader for older Streamlit versions.
    """
    try:
        audio_bytes = st.audio_input("🎤 Record your answer", key=key)
        return audio_bytes  # UploadedFile or None
    except AttributeError:
        st.warning("⚠️ Please upgrade Streamlit: `pip install --upgrade streamlit`")
        uploaded = st.file_uploader(
            "Upload an audio file (.wav / .mp3)",
            type=["wav", "mp3", "ogg", "webm"],
            key=f"{key}_upload"
        )
        return uploaded


def clear_audio(key):
    """Reset the audio widget for the next question."""
    if key in st.session_state:
        del st.session_state[key]
    upload_key = f"{key}_upload"
    if upload_key in st.session_state:
        del st.session_state[upload_key]