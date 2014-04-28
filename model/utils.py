from elo.model import EloModel
from model.models import UserSkill, QuestionDifficulty, DatabaseDataProvider
from questions.models import Answer


def update_user_skillxxx(response, expected_response, user_skill, question_type):
    parent_skill = user_skill.skill.parent
    if parent_skill:
        user_parent_skill, _ = UserSkill.objects.get_or_create(user=user_skill.user, skill=parent_skill)
        update_user_skillxxx(response, expected_response, user_parent_skill, question_type)

    user_skill.save()



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
    Process all answers - can by really slow
    """
    QuestionDifficulty.objects.all().delete()
    UserSkill.objects.all().delete()

    answers = Answer.objects.all().select_related("question__skill").order_by('timestamp')

    for answer in answers:
        process_answer(answer)