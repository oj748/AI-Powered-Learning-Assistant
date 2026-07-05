from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_pdf_gemini(pdf_path):

    uploaded = client.files.upload(
        file=pdf_path
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=[
            uploaded,
            """
Extract all readable text from this PDF.

Rules:
- Preserve page order.
- Ignore headers/footers if repetitive.
- Preserve tables as Markdown tables.
- Preserve headings.
- Preserve numbered and bulleted lists.
- Preserve mathematical expressions using LaTeX where appropriate.
- Do not add explanations.
- If text is unreadable, omit it rather than guessing.   
"""
        ]
    )

    return response.text.strip()