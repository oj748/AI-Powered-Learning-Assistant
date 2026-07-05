from services.phi4 import get_phi

def summarize_text(text):
    phi = get_phi()
    prompt = f"""

The input may contain lecture transcripts, textbook notes, programming examples, mathematical derivations, or code.

Your task is to convert them into concise study notes suitable for revision.

Instructions:

- Read the transcript.
- Do NOT copy the transcript.
- Do NOT quote large sections.
- Rewrite everything in your own words.
- Keep only important information.
- Remove repetition.
- Remove filler.
- Organize the notes.

Output format:

# Title

## Summary

(3-5 sentences)

## Key Concepts

- ...

## Important Definitions

- ...

## Important Facts

- ...

## Syntax / Formulae

(Only if present.)

If the study material contains source code:

- Treat code as supporting examples.
- Do NOT summarize code line-by-line.
- Do NOT reproduce entire programs.
- Mention only what the program demonstrates.
- Include at most one very small code snippet (3-8 lines) if it is essential to understanding the concept.
- Ignore repetitive implementation details.
- Never invent code examples.
- Never complete or extend partial programs.

Ignore sections titled:

- Important Questions
- Practice Questions
- Exercises
- Assignments
- Viva Questions
unless they introduce new concepts.

Return ONLY the Markdown notes.

BEGIN TRANSCRIPT

{text}

END TRANSCRIPT
"""

    return phi.ask(prompt, max_tokens=1000)
