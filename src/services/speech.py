from config import MODELS_DIR

MODEL_PATH = (
    MODELS_DIR
    / "whisper"
)

whisper = None

def load_whisper():

    global whisper

    if whisper is None:
        from faster_whisper import WhisperModel
        print("Loading Whisper...")

        whisper = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8",
            download_root = str(MODEL_PATH)
        )

        print("Whisper loaded.")

    return whisper

def transcribe_audio(audio_file):

    model = load_whisper()

    segments, info = model.transcribe(
        audio_file,
        language="en",
        beam_size=1
    )

    return segments, info
