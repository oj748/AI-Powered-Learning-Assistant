from services.schema import QuizQuestion
from services.gemini import ask

def create_quiz_online(text):

    prompt = f"""
Create a quiz from the study material.

Requirements:

- Create 5–10 multiple-choice questions.
- Each question must test one important concept.
- Each question must have exactly four options.
- Do not include option labels (like "A.", "B.", "C.", or "D.") in the output.
- Only one option should be correct.
- Use the `correct` field to specify the correct option as "A", "B", "C", or "D".
- Include a short explanation (1–3 sentences).
- Include a mixture of easy, medium and difficult questions.
- Focus on understanding, reasoning and application rather than memorization.
- Questions should be self-contained.
- Do not invent information that is not present in the study material.
- If mathematical expressions are present, use LaTeX notation.
- Do not include any URLs in any of the questions or answers.

Study Material:

{text}
"""
    response = ask(
        prompt,
        schema=list[QuizQuestion]
    )
    return response