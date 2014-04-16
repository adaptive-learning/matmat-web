import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from lazysignup.decorators import allow_lazy_user
from model.elo import process_answer

from questions.models import Question, Answer, Simulator


@ensure_csrf_cookie
@allow_lazy_user
def play(request):
    simulators = Simulator.objects.all()

    return render(request, 'questions/play.html', {
        "simulators": simulators,
    })


def get_question(request):
    questions = Question.objects.all().select_related("simulator").order_by("?")[:request.GET["count"]]
    return HttpResponse(json.dumps([q.as_json() for q in questions]))


def save_answer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        answer = Answer.objects.create(
            question_id=data["pk"],
            user=request.user,
            log=data["log"],
            solving_time=data["time"],
            correctly_solved=data["correctly_solved"],
        )
        process_answer(answer)

    return HttpResponse("Have to be POST")