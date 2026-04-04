from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av

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
    )

    if ctx.audio_processor:
        return ctx.audio_processor.frames
    return None