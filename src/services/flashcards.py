from services.phi4 import get_phi
from services.json_utils import parse_llm_json
from services.schema import Flashcard


def create_flashcard(text):

    phi = get_phi()

    prompt = f"""
You are an expert teacher.

Study the material below and create flashcards that promote understanding rather than memorization.

Rules:

Requirements:

- Create 5 flashcards.
- Each flashcard should test exactly one important concept.
- Focus on definitions, reasoning, applications, comparisons, formulas, and cause-and-effect relationships.
- Questions should be self-contained and understandable without seeing the original notes.
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

Schema:

[
    {{
        "question": "Question text",
        "answer": "Answer text"
    }}
]

IMPORTANT:

- First character must be [
- Last character must be ]
- Return only valid JSON
- Every JSON string must be properly escaped.

Write LaTeX using escaped backslashes. For example:
Correct:
\\\\theta
\\\\frac
\\\\bar
\\\\text

Never output:
\\theta
\\frac
\\bar
\\text

Study Material:

{text}
"""

    response = phi.ask(prompt, max_tokens=2000)
    response = parse_llm_json(response)
    cards = [
        Flashcard(
            **{k.lower(): v for k, v in card.items()}
        ).model_dump()
        for card in response
    ]
    return cards