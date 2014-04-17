from questions.models import Question


def recommend_questions(user, skills):
    questions = Question.objects.filter().select_related("simulator")\
        .filter(skill__in=skills)\

    return questions
