import os
from PIL import Image
import time
from config import PROJECT_ROOT

os.environ["PADDLE_HOME"] = f"{PROJECT_ROOT}/models"

ocr = None


def preload_ocr():
    global ocr
    start = time.time()
    if ocr is None:

        from paddleocr import PaddleOCR

        ocr = PaddleOCR(
            lang="en",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            enable_mkldnn=False,
            cpu_threads=2,
        )
    print("Preloaded OCR in ", time.time() - start)

def resize_for_ocr(path):

    img = Image.open(path)

    max_dim = 1200

    width, height = img.size

    largest_dim = max(width, height)

    if largest_dim > max_dim:

        scale = max_dim / largest_dim

        new_width = int(width * scale)
        new_height = int(height * scale)

        img = img.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        temp_path = "temp_ocr.jpg"

        img.save(
            temp_path,
            quality=90,
            optimize=True
        )

        print(f"Resized OCR image: {width}x{height} -> {new_width}x{new_height}")

        return temp_path

    print(f"OCR image unchanged: {width}x{height}")

    return path

def extract_text(path):

    global ocr

    path = resize_for_ocr(path)

    start = time.time()

    if ocr is None:
       preload_ocr()

    result = ocr.predict(path)

    print("OCR finished in ", time.time() - start)
    text = []

    for page in result:
        text.extend(page["rec_texts"])

    return "\n".join(text)