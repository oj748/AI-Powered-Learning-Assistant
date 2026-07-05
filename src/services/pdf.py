import fitz
import tempfile
import os

from services.ocr import extract_text
from services.spell_checker import spell_check


def extract_pdf(pdf_path):
    """
    Yields:
        (page_number, total_pages, page_text)

    Each page is processed independently. If a page already contains
    embedded text, it is extracted directly. Otherwise the page is
    rendered as an image and passed through the existing OCR pipeline.
    """

    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    try:
        for page_number, page in enumerate(doc, start=1):

            # ---------- Try extracting embedded text ----------
            text = page.get_text().strip()

            # ---------- OCR fallback ----------
            if not text:

                pix = page.get_pixmap(dpi=300)

                with tempfile.NamedTemporaryFile(
                    suffix=".png",
                    delete=False
                ) as tmp:

                    temp_path = tmp.name

                try:
                    pix.save(temp_path)

                    raw_text = extract_text(temp_path)
                    text = spell_check(raw_text)

                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

            yield page_number, total_pages, text

    finally:
        doc.close()