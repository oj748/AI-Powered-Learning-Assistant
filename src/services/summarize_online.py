from services.gemini import ask


def summarize_online(transcript):

    prompt = f"""
You are an expert teacher.

Study the transcript below and create detailed study notes.

Requirements:

- Return Markdown only.
- Use headings and subheadings.
- Use bullet points where appropriate.
- Use tables if useful.
- Use LaTeX ($...$ or $$...$$) for mathematics.
- Do not use HTML.

At the end, add a section called "Further Learning" containing:

1. Three recommended online learning resources (books, university courses, or reputable websites).
2. Two or three relevant YouTube channels or videos if appropriate.
3. Five related concepts the student should study next along with recommended resources.
The format for these should be:
- Resource name
- URL
- One sentence explaining why it is useful

Only recommend high-quality educational resources.

Transcript:

{transcript}
"""

    return ask(prompt)