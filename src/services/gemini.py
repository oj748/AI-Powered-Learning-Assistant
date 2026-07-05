from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask(prompt, schema=None):

    config = None

    if schema is not None:
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema
        )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=config
    )

    if schema is not None:
        parsed = response.parsed

        if isinstance(parsed, list):
            return [obj.model_dump() for obj in parsed]

        return parsed.model_dump()

    return response.text.strip()