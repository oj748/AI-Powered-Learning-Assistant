from services.phi4 import get_phi

def spell_check(text):
    phi = get_phi()
    prompt = f"""
Correct OCR errors.

Rules:
- Identify the main idea of the text
- Fix spelling mistakes caused by OCR keeping the main idea in mind.
- Preserve meaning.
- Return only corrected text.
- Do not summarize.
- If the words look confusing, use the context of the text to predict the words

TEXT:

{text}
"""

    return phi.ask(prompt, max_tokens=1000)
