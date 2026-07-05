from PySide6.QtCore import QThread, Signal
import os
from services.ocr import extract_text
from services.spell_checker import spell_check
print("gemini imports started")
from services.ocr_gemini import extract_text_gemini

class OCRWorker(QThread):

    finished = Signal(str)
    progress = Signal(str)
    partial_transcript = Signal(str)

    def __init__(self, image_paths,online=False):
        super().__init__()
        self.online = online
        self.image_paths = image_paths

    def run(self):
        transcript_parts = []
        for i, path in enumerate(self.image_paths, start=1):
            self.progress.emit(
                f"Extracting text from image {i}/{len(self.image_paths)} ({os.path.basename(path)})"
            )
            if self.online:
                try:
                    raw_text = extract_text_gemini(path)
                    print("Gemini is workingggg")
                except Exception as e:
                    self.progress.emit(
                        "Online OCR unavailable. Falling back to local OCR..."
                    )
                    print("failed :",e)
                    raw_text = self._offline_ocr(path)
            else:
                self.progress.emit(
                    "Offline mode selected."
                )
                raw_text = self._offline_ocr(path)

            self.partial_transcript.emit(f"\n\n{raw_text}")

            transcript_parts.append(raw_text)

        self.finished.emit("\n\n".join(transcript_parts))

    def _offline_ocr(self, path):

        self.progress.emit(
            "Using local OCR..."
        )

        raw_text = extract_text(path)

        self.progress.emit(
            "Correcting OCR errors..."
        )

        return spell_check(raw_text)