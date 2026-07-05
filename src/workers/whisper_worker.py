from PySide6.QtCore import QThread, Signal
from services.speech import transcribe_audio

class WhisperWorker(QThread):

    progress = Signal(str)
    partial_transcript = Signal(str)
    finished = Signal(str)

    def __init__(self, files):
        super().__init__()
        self.files = files

    def run(self):

        transcripts = []

        total = len(self.files)

        for i, file in enumerate(self.files, start=1):

            text = []
            segments, info = transcribe_audio(file)

            for segment in segments:
                text.append(segment.text)
                percent = int(
                    segment.end / info.duration * 100
                )
                print(
                    f"{file} | "
                    f"segment.end={segment.end:.2f} | "
                    f"duration={info.duration:.2f} | "
                    f"{percent}%"
                )
                self.partial_transcript.emit(
                    segment.text
                )

                self.progress.emit(
                    f"Transcribing audio {i}/{total} ..... {percent}%"
                )

            transcripts.append(" ".join(text))

        self.finished.emit("\n\n".join(transcripts))