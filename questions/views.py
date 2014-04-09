import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from questions.models import Question


@ensure_csrf_cookie
def play(request):
    return render(request, 'questions/play.html')


def get_question(request):
    question = Question.objects.all().order_by("?")[0]
    return HttpResponse(json.dumps(question.as_json()))


def save_answer(request):
    if request.method == "POST":
        data = json.loads(request.body)


    return HttpResponse("Have to be POST")