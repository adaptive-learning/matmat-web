import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from lazysignup.decorators import allow_lazy_user
from model.utils import process_answer, recalculate_model
from model.models import Skill
from model.recommendation import recommend_questions

from questions.models import Question, Answer, Simulator


@ensure_csrf_cookie
@allow_lazy_user
def play(request):
    simulators = Simulator.objects.all()

    return render(request, 'questions/play.html', {
        "simulators": simulators,
    })


def get_question(request):
    """
    load questions from server as jason
    """
    skill = get_object_or_404(Skill, pk=request.GET["skill"])
    subskills = skill.children_list
    in_queue = [] if request.GET["in_queue"] == "" else request.GET["in_queue"].split(",")

    questions = recommend_questions(int(request.GET["count"]), request.user, subskills, in_queue)

    return HttpResponse(json.dumps([q.as_json() for q in questions]))


def get_question_test(request):
    """
    test page for question recommendation
    """
    skill = get_object_or_404(Skill, pk=request.GET["skill"])
    subskills = skill.children_list
    in_queue = [] if request.GET["in_queue"] == "" else request.GET["in_queue"].split(",")

    questions = recommend_questions(int(request.GET["count"]), request.user, subskills, in_queue)

    return render(request, 'questions/get_question_test.html', {
        "questions": questions
    })


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
