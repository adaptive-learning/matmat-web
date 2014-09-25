import json
from django import forms
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
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

@login_required
def get_questions(request):
    """
    load recommended questions from server as jason
    """
    skill = get_object_or_404(Skill, pk=request.GET["skill"])
    subskills = skill.children_list
    in_queue = [] if request.GET["in_queue"] == "" else request.GET["in_queue"].split(",")

    questions = recommend_questions(int(request.GET["count"]), request.user, subskills, in_queue)

    return HttpResponse(json.dumps([q.as_json() for q in questions]))


def get_selected_question(request, question_pk):
    q = get_object_or_404(Question, pk=question_pk)
    return HttpResponse(json.dumps([q.as_json()]))

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
    """
    save answer to question and process it
    """
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


class SimulatorTestView(View):
    """
    test page for question recommendation
    """
    def get(self, request):
        simulator=None
        if "simulator" in request.GET and request.GET["simulator"] != "":
            # skill = request.GET["skill"]
            simulator = request.GET["simulator"]
            questions = Question.objects.filter(player_id=simulator)
            form = SelectSkillForm(request.GET)
            form.fields["question"] = forms.ModelChoiceField(queryset=questions, required=False,
                                                             widget=forms.Select(attrs={"onChange": "submit()"}))
            form.fields["own_question"] = forms.CharField(initial="{}", required=False, )
        else:
            form = SelectSkillForm()

        own_question = None
        simulator_name = None
        if "own_question" in request.GET and request.GET["own_question"] != "":
            own_question = request.GET["own_question"]
            simulator_name = get_object_or_404(Simulator, pk=simulator).name

        question = None
        if "question" in request.GET and request.GET["question"] != "":
            question = request.GET["question"]
            question = get_object_or_404(Question, pk=question)
        if question is None or str(question.player.pk) != simulator:
            if Question.objects.filter(player=simulator).count() > 0:
                question = Question.objects.filter(player=simulator)[0]

        return render(request, 'questions/simulator_test.html', {
            "form": form,
            "question": question,
            "own_question": own_question,
            "simulator": simulator_name,
            "simulators": Simulator.objects.all(),
        })

simulator_test = SimulatorTestView.as_view()


class SelectSkillForm(forms.Form):
    # skill = forms.ModelChoiceField(queryset=Skill.objects.all())
    simulator = forms.ModelChoiceField(queryset=Simulator.objects.all(), required=True
                                       , widget=forms.Select(attrs={"onChange": "submit()"}))