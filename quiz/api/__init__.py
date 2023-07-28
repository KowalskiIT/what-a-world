from requests import get

DIFFICULTY = ('easy', 'medium', 'hard')
MAX_QUESTIONS = 50


class ApiClient:
    CATEGORIES_URL = "https://opentdb.com/api_category.php"
    QUESTIONS_URL = "https://opentdb.com/api.php?amount={}&category={}&difficulty={}"
    QUESTIONS_AMOUNT = "https://opentdb.com/api_count.php?category={}"

    @classmethod
    def get_quiz_options(cls) -> dict:
        result = {'categories': get(ApiClient.CATEGORIES_URL).json()['trivia_categories'],
                  'max_questions': MAX_QUESTIONS,
                  'difficulty': DIFFICULTY}
        return result

    @classmethod
    def get_questions(cls, difficulty: str, max_questions: int, category: int) -> dict:
        return get(ApiClient.QUESTIONS_URL.format(max_questions, category, difficulty)).json()['results']

    @classmethod
    def get_questions_amount(cls, category: int, difficulty: str):
        cat_question_amount = get(ApiClient.QUESTIONS_AMOUNT.format(category)).json()['category_question_count']
        return cat_question_amount[f'total_{difficulty}_question_count']
