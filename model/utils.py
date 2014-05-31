import json
from django.db import connection
import math
from elo.DataProviderInterface import DataProviderInterface
from elo.model import EloModel
from model.models import UserSkill, QuestionDifficulty, DatabaseDataProvider, Skill
from questions.models import Question


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    for row in cursor.fetchall():
        yield dict(zip([col[0] for col in desc], row))

def process_answer(answer):
    """
    Update model considering this answer
    """
    provider = DatabaseDataProvider()
    elo = EloModel(provider)
    provider.set_answer(answer)
    elo.update()


def recalculate_model():
    """
    Process all answers
    """


    cursor = connection.cursor()
    cursor.execute(
        "SELECT "
            "questions_answer.id, "
            "questions_answer.question_id as question, "
            "questions_answer.user_id as user, "
            "questions_answer.solving_time, "
            "questions_answer.correctly_solved "
        "FROM questions_answer "
        "ORDER BY questions_answer.timestamp ASC")

    provider = CachingDatabaseDataProvider()
    init_difficulty(provider)
    elo = EloModel(provider)
    for answer in dictfetchall(cursor):
        provider.set_answer(answer)
        elo.update()

    QuestionDifficulty.objects.all().delete()
    UserSkill.objects.all().delete()
    provider.save_data()


def init_difficulty(data):
    for question in data.get_questions():
        question_data = data.get_questions_data(question)
        question_data = json.loads(question_data)
        if "answer" in question_data.keys():
            value = abs(float(question_data["answer"]))
            if value <= 0:
                value = 1
            value = math.log(value) - 3
            data.set_difficulty(question, value)
        else:
            print "answer not found"



class CachingDatabaseDataProvider(DataProviderInterface):
    def __init__(self):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
                "questions_question.id as pk, "
                "questions_question.skill_id as skill, "
                "questions_question.data as data, "
                "questions_question.type "
            "FROM questions_question "
            "LEFT OUTER JOIN model_questiondifficulty ON ( questions_question.id = model_questiondifficulty.question_id )"
        )
        self.questions = {}
        for q in dictfetchall(cursor):
            self.questions[q["pk"]] = q

        cursor.execute(
            "SELECT "
                "model_skill.id as pk, "
                "model_skill.parent_id as parent "
            "FROM model_skill "
        )
        self.skills = {}
        for q in dictfetchall(cursor):
            self.skills[q["pk"]] = q

        self.user_skills = {}
        self.attempts_count = {}

    def save_data(self):
        data = []
        for pk, q in self.questions.items():
            if "difficulty" in q.keys() and q["difficulty"] is not None:
                data.append(QuestionDifficulty(question_id=pk, value=q["difficulty"]))
        QuestionDifficulty.objects.bulk_create(data)

        data = []
        for user, d in self.user_skills.items():
            for skill, value in d.items():
                data.append(UserSkill(user_id=user, skill_id=skill, value=value))
        UserSkill.objects.bulk_create(data)


    def set_answer(self, answer):
        super(CachingDatabaseDataProvider, self).set_answer(answer)
        self.mark_attempt(answer)

    def mark_attempt(self, answer):
        user = self.get_user(answer)
        question = self.get_question(answer)
        if question not in self.attempts_count.keys():
            self.attempts_count[question] = {}
        if user not in self.attempts_count[question].keys():
            self.attempts_count[question][user] = 1
        else:
            self.attempts_count[question][user] += 1

    def get_question(self, answer):
        return answer["question"]

    def get_user(self, answer):
        return answer["user"]

    def get_skill(self, question):
        return self.questions[question]["skill"]

    def get_question_type(self, question):
        return self.questions[question]["type"]

    def get_user_skill(self, user, skill):
        try:
            return self.user_skills[user][skill]
        except:
            return None

    def set_user_skill(self, user, skill, value):
        if user not in self.user_skills.keys():
            self.user_skills[user] = {}
        self.user_skills[user][skill] = value

    def get_parent_skill(self, skill):
        return self.skills[skill]["parent"]

    def get_difficulty(self, question):
        try:
            return self.questions[question]["difficulty"]
        except:
            return None

    def set_difficulty(self, question, value):
        self.questions[question]["difficulty"] = value

    def get_solving_time(self, answer):
        return answer["solving_time"]

    def get_correctness(self, answer):
        return answer["correctly_solved"]

    def is_first_attempt(self, answer):
        user = self.get_user(answer)
        question = self.get_question(answer)
        try:
            return self.attempts_count[question][user] < 2
        except:
            return True

    def get_first_attempts_count(self, question):
        count = 0
        for _, v in self.attempts_count[question].items():
            count += v
        return count

    def get_questions(self):
        return self.questions.keys()

    def get_questions_data(self, question):
        return self.questions[question]["data"]