from math import sqrt
from model.elo import get_expected_response
from questions.models import Question


def recommend_questions(user, skills, in_queue):
    questions = Question.objects.raw(
        "SELECT questions_question.*, "
        "COUNT(questions_answer.id) AS answers_count, "
        "MIN(TIME_TO_SEC(TIMEDIFF(NOW(), questions_answer.timestamp))) AS time_form_last_answer,"
        "model_userskill.value as user_skill, "
        "model_questiondifficulty.value as questiondifficulty "
        "FROM questions_question "
        "LEFT JOIN model_userskill ON ( model_userskill.skill_id = questions_question.skill_id AND model_userskill.user_id = %(user_id)s)"
        "LEFT JOIN questions_answer ON ( questions_question.id = questions_answer.question_id AND questions_answer.user_id = %(user_id)s) "
        "LEFT JOIN model_questiondifficulty ON ( model_questiondifficulty.question_id = questions_question.id) "
        "WHERE questions_question.skill_id IN ( {0} ) {1} "
        "GROUP BY questions_question.id ".format(
            skills,
            "AND questions_question.id NOT IN ( {0} ) ".format(",".join(in_queue)) if in_queue else ""
        ),
        {
            "user_id": user.pk,

         }
    )
    questions = list(questions)
    questions.sort(key=lambda q: question_priority(q, user.is_staff), reverse=True)

    return questions


def question_priority(question, log):
    GOAL_RESPONSE = 0.7
    TIME_WEIGHT = 120
    COUNT_WEIGHT = 2
    ESTIMATE_WEIGHT = 10

    difficulty = question.questiondifficulty if question.questiondifficulty is not None else 0

    count_score = 1. / (sqrt(1 + question.answers_count))
    if question.time_form_last_answer is None:
        time_score = 0
    else:
        time_score = -1. / (question.time_form_last_answer) if question.time_form_last_answer > 0 else -1

    user_skill = question.user_skill if question.user_skill is not None else 0 # TODO predelat
    expected_response = get_expected_response(user_skill, difficulty, question.type)
    if GOAL_RESPONSE > expected_response:
        estimate_score = expected_response / GOAL_RESPONSE
    else:
        estimate_score = (1 - expected_response) / (1 - GOAL_RESPONSE)

    priority = count_score * COUNT_WEIGHT + time_score * TIME_WEIGHT + estimate_score * ESTIMATE_WEIGHT

    if log:
        question.recommendation_log = {
            "count_score": "{0} * {1} = {2}".format(count_score, COUNT_WEIGHT, count_score * COUNT_WEIGHT),
            "time_score": "-{1} / {0}  = {2}".format(question.time_form_last_answer, TIME_WEIGHT, time_score * TIME_WEIGHT),
            "estimate_score": "{0} * {1} = {2}".format(estimate_score, ESTIMATE_WEIGHT, estimate_score * ESTIMATE_WEIGHT),
            "expected_response": expected_response,
            "total": priority,
        }

    return priority
