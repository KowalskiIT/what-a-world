from ..api import ApiClient
from typing import List
from dataclasses import dataclass, field
from random import shuffle
from html import unescape
import logging as log


@dataclass
class Question:
    category: str
    type: str
    difficulty: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]
    answers: List[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.answers.extend(self.incorrect_answers)
        self.answers.append(self.correct_answer)
        shuffle(self.answers)
        self.question = unescape(self.question)

    def check_answer(self, answer: str):
        return answer == self.correct_answer


@dataclass
class Quiz:
    number_of_questions: int
    difficulty: str
    questions: List[Question]
    current_question: int
    number_of_correct_answers: int
    just_started: bool = True

    @classmethod
    def create_game(cls, number_of_questions, difficulty, category):
        available_question_number = ApiClient.get_questions_amount(category, difficulty)

        if int(number_of_questions) <= available_question_number:
            raw_questions = ApiClient.get_questions(difficulty, number_of_questions, category)
        else:
            raw_questions = ApiClient.get_questions(difficulty, available_question_number, category)
        questions = list([Question(**raw_question) for raw_question in raw_questions])
        return Quiz(number_of_questions, difficulty, questions, 0, 0)

    def save(self, request):
        request.session['saved_quiz'] = self

    def stop(self, request):
        del request.session['saved_quiz']

    @classmethod
    def restore(cls, request):
        return request.session.get('saved_quiz')

    def get_question(self):
        if not self.just_started:
            self.current_question += 1
        question = self.questions[self.current_question]
        return question

    def check_answer(self, answer):
        if answer:
            self.just_started = False
        if self.questions[self.current_question].correct_answer == answer:
            self.number_of_correct_answers += 1

    def get_result(self):
        return {
            'correct_answers': self.number_of_correct_answers,
            'all_questions': len(self.questions)
        }
