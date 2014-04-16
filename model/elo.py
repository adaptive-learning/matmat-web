import math
from model.models import UserSkill, QuestionDifficulty
from questions.models import Answer

INITIAL_DIFFICULTY = 0


def get_expected_response(user_skill, difficulty, question_type):
    if question_type == 'c':
        return 1. / (1 + math.exp(difficulty.value - user_skill.value))
    if question_type == 't':
        return -(user_skill - difficulty)


def get_response(answer, question_type):
    if question_type == 'c':
        return 1 * answer.correctly_solved
    if question_type == 't':
        return math.log(answer.solving_time)


def update_user_skill(response, expected_response, user_skill, question_type):
    K = 1

    if question_type == 'c':
        user_skill.value += K * (response - expected_response)
    if question_type == 't':
        user_skill.value += K * (expected_response - response)

    # TODO update parent skills

    user_skill.save()


def update_difficulty(response, expected_response, difficulty, question_type):
    ALPHA = 1.0
    DYNAMIC_ALPHA = 0.05
    K = ALPHA / (1 + DYNAMIC_ALPHA * (difficulty.get_first_attempts_count() - 1))

    if question_type == 'c':
        difficulty.value += K * (expected_response - response)      # that is K * ((1 - response) - (1 - expected_response))
    if question_type == 't':
        difficulty.value += K * (response - expected_response)

    difficulty.save()


def process_answer(answer):
    """
    Update model considering this answer
    """
    skill = answer.question.skill
    question_type = answer.question.type
    try:
        difficulty = answer.question.difficulty
    except QuestionDifficulty.DoesNotExist:
        difficulty = QuestionDifficulty.objects.create(question=answer.question, value=INITIAL_DIFFICULTY)
    user_skill, _ = UserSkill.objects.get_or_create(user=answer.user, skill=skill)

    expected_response = get_expected_response(user_skill, difficulty, question_type=question_type)
    response = get_response(answer, question_type)

    update_user_skill(response, expected_response, user_skill, question_type)
    if answer.is_first_attempt():
        update_difficulty(response, expected_response, difficulty, question_type)


def recalculate_model():
    """
    Process all answers - can by really slow
    """
    QuestionDifficulty.objects.all().delete()
    UserSkill.objects.all().delete()

    answers = Answer.objects.all().select_related("question__skill").order_by('timestamp')

    for answer in answers:
        process_answer(answer)