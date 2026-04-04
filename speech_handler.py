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
        async_processing=True,
        audio_processor_factory=AudioProcessor
    )

    # store context for clearing later
    st.session_state[f"{key}_ctx"] = ctx

    # directly read frames (no session_state dependency)
    if ctx and ctx.audio_processor:
        frames = ctx.audio_processor.frames
        if isinstance(frames, list):
            return frames

    return []