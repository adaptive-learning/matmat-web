import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from lazysignup.decorators import allow_lazy_user

from questions.models import Question, Answer


@ensure_csrf_cookie
@allow_lazy_user
def play(request):
    return render(request, 'questions/play.html')


def get_question(request):
    question = Question.objects.all().order_by("?")[0]
    return HttpResponse(json.dumps(question.as_json()))


def save_answer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print request.user.pk
        Answer.objects.create(
            question_id=data["pk"],
            user=request.user,
            log=data["log"],
            solving_time=data["time"],
            correctly_solved=data["correctly_solved"],
        )

    return HttpResponse("Have to be POST")