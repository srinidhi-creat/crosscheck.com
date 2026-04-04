from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import streamlit as st

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame):
        self.frames.append(frame)
        return frame


def record_audio(key):
    ctx = webrtc_streamer(
        key=key,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,  # 🔥 important
    )

    if ctx.audio_processor:
        frames = ctx.audio_processor.frames

        # only store if meaningful audio exists
        if len(frames) > 0:
            st.session_state[key] = frames

    return st.session_state.get(key, [])