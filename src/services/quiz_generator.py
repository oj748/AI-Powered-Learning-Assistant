from services.phi4 import get_phi

from services.json_utils import parse_llm_json


def create_quiz(text):
    phi = get_phi()
    prompt = f"""
    You are generating a multiple-choice quiz from study material.

    ## Task

    Create exactly 5 multiple-choice questions.

    ## Requirements

    - Each question must have exactly 4 options.
    - Exactly one option must be correct.
    - Do not include option labels (like "A.", "B.", "C.", or "D.") in the output.
    - The "correct" field must contain ONLY one letter: "A", "B", "C", or "D".
    - Include a short explanation (1 sentence preferred, maximum 2 sentences).
    - Cover key concepts, reasoning, comparisons, applications, and problem solving.
    - Include a mixture of easy, medium, and difficult questions.
    - Do not copy sentences directly from the study material.
    - Do not invent facts that are not present in the study material.
    - If the material contains mathematics, preserve all mathematical notation.
    - Write mathematical expressions using LaTeX:
      - Inline: $...$
      - Display: $$...$$
    - Do not invent mathematical formulas if none exist.
    - Do not include URLs.
    - For software-related content, assess understanding—not implementation. Convert code examples into conceptual questions and avoid asking learners to write or recall code, syntax, APIs, commands, or other implementation details.
    ## Output Rules

    Return ONLY a valid JSON array.

    The response:
    - MUST begin with '['
    - MUST end with ']'
    - MUST contain no Markdown
    - MUST contain no explanations outside the JSON
    - MUST contain no ```json fences

    Escape every JSON string correctly.
    Escape every LaTeX backslash correctly.

    ## JSON Format

    [
      {{
        "question": "Question text",
        "options": [
          "Option A",
          "Option B",
          "Option C",
          "Option D"
        ],
        "correct": "A",
        "explanation": "Brief explanation."
      }}
    ]

    Study Material:

    {text}
    """
    response = phi.ask(prompt, max_tokens=2000)
    print(response)
    response = parse_llm_json(response)
    return response