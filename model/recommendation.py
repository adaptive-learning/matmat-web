from math import sqrt
from model.elo import get_expected_response
from questions.models import Question

def recommend_questions(user, skills):

    questions = Question.objects.raw(
        "SELECT questions_question.*, "
        "COUNT(questions_answer.id) AS answers_count, "
        "MIN(TIME_TO_SEC(TIMEDIFF(NOW(), questions_answer.timestamp))) AS time_form_last_answer,"
        "model_userskill.value as user_skill, "
        "model_questiondifficulty.* "
        "FROM questions_question "
        "LEFT JOIN model_userskill ON ( model_userskill.skill_id = questions_question.skill_id AND model_userskill.user_id = %(user_id)s)"
        "LEFT JOIN questions_answer ON ( questions_question.id = questions_answer.question_id AND questions_answer.user_id = %(user_id)s) "
        "LEFT JOIN model_questiondifficulty ON ( model_questiondifficulty.question_id = questions_question.id) "
        "WHERE questions_question.skill_id IN ( {0} ) "
        "GROUP BY questions_question.id ".format(",".join([str(s.pk) for s in skills])),
        {
            "user_id": user.pk,
         }
    )
    questions = list(questions)
    questions.sort(key=question_priority, reverse=True)

    return questions


def question_priority(question):
    GOAL_RESPONSE = 0.7
    TIME_WEIGHT = 120
    COUNT_WEIGHT = 2
    ESTIMATE_WEIGHT = 10

    count_score = 1 / (sqrt(1 + question.answers_count))
    time_score = -1 / (question.time_form_last_answer) if question.time_form_last_answer > 0 else -1

    user_skill = question.user_skill if question.user_skill is not None else 0 # TODO predelat
    expected_response = get_expected_response(user_skill, question.difficulty.value, question.type)
    if GOAL_RESPONSE > expected_response:
        estimate_score = expected_response / GOAL_RESPONSE
    else:
        estimate_score = (1 - expected_response) / (1 - GOAL_RESPONSE)

    return count_score * COUNT_WEIGHT + time_score * TIME_WEIGHT + estimate_score * ESTIMATE_WEIGHT