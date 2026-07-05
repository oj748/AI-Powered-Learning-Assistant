from services.schema import Flashcard
from services.gemini import ask


def create_flashcard_online(text):
    prompt = f"""

Study the material below and create flashcards that promote understanding rather than memorization.

Requirements:
You are a study assistant
- Create 5 to 10 flashcards.
- Every flashcard must be related to the text, but not so much that the flashcard cannot be understood without the context of the text. 
- Each flashcard should test exactly one important concept.
- Focus on definitions, reasoning, applications, comparisons, formulas, and cause-and-effect relationships.
- Answers should be concise (1–3 sentences) while remaining complete.
- If mathematical expressions are present, write them using LaTeX syntax (inline: $...$, display: $$...$$).
- Preserve mathematical notation, symbols, variables, and units accurately.
- Do not include explanations or commentary outside the JSON.
- Do not invent information that is not supported by the study material.
- If the study material contains no mathematics, do not invent formulas.
- Do not include any URLs in any of the questions or answers.

Programming Material:

If the study material contains source code, programming examples, algorithms, APIs, or software development concepts:
- Treat the code as an example used to explain concepts.
- Generate flashcards that test understanding of concepts, reasoning, design decisions, architecture, debugging, and real-world applications.
- Do NOT ask the learner to write code.
- Do NOT ask the learner to reproduce algorithms, programs, SQL queries, shell commands, regex, or syntax from memory.
- Do NOT ask for function signatures, method names, parameter lists, library names, or exact API usage unless they are themselves the concept being taught.
- Do NOT ask questions beginning with "Write...", "Implement...", "Code...", "Program...", or "Develop...".
- Convert implementation examples into conceptual questions.
    
Return ONLY valid JSON.

IMPORTANT:

- First character must be [
- Last character must be ]
- Return only valid JSON
- Every JSON string must be properly escaped.
- Every LaTeX backslash must be escaped.

Study Material:
{text}
"""

    response = ask(
        prompt,
        schema=list[Flashcard]
    )

    return response