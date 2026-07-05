import os
import time
start = time.time()
from google import genai
print("genai imported: ", time.time() - start)
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

from google.genai import types
import mimetypes

def extract_text_gemini(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = """
    Extract all visible text from this image.
    Do not summarize.
    Return the extracted text as valid Markdown.

- Preserve tables as Markdown tables.
- Preserve headings.
- Preserve numbered and bulleted lists.
- Preserve mathematical expressions using LaTeX where appropriate.
- Do not add explanations.
- If text is unreadable, omit it rather than guessing.   
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=[
            prompt,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            )
        ]
    )

    print(response)
    print("TEXT:", response.text)

    if response.text is None:
        raise RuntimeError(f"Gemini returned no text.\n{response}")

    return response.text.strip()
