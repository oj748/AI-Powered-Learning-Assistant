from PySide6.QtCore import QThread, Signal
import os

from services.pdf import extract_pdf
from services.pdf_online import extract_pdf_gemini


class PDFWorker(QThread):

    finished = Signal(str)
    progress = Signal(str)
    partial_transcript = Signal(str)

    def __init__(self, pdf_path, online=False):
        super().__init__()

        self.pdf_path = pdf_path
        self.online = online

    def run(self):

        self.progress.emit(
            f"Reading {os.path.basename(self.pdf_path)}"
        )

        if self.online:

            try:

                self.progress.emit(
                    "Uploading PDF to Gemini..."
                )

                text = extract_pdf_gemini(self.pdf_path)

                self.partial_transcript.emit(text)

                self.finished.emit(text)

                return

            except Exception as e:

                print(e)

                self.progress.emit(
                    "Online extraction failed. Using offline mode..."
                )

        # ---------- Offline ----------
        transcript = []

        for page_no, total, text in extract_pdf(self.pdf_path):
            self.progress.emit(
                f"Processing page {page_no}/{total}"
            )

            self.partial_transcript.emit(
                f"\n\n{text}"
            )

            transcript.append(text)

        self.finished.emit("\n\n".join(transcript))