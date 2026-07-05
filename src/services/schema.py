from pydantic import BaseModel
from typing import Literal

class Flashcard(BaseModel):
    question: str
    answer: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct : Literal["A", "B", "C", "D"]
    explanation: str