from math import e
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django import forms
from django.db.models import Avg, Count, Max
from django.shortcuts import render
from core.models import UserProfile
from model.models import Skill, UserSkill, QuestionDifficulty
from model.views import get_style
from questions.models import Question, Answer


@staff_member_required
def overview(request):

    return render(request, 'administration/overview.html',{
        "lazy_users": User.objects.filter(lazyuser__isnull=False).count(),
        "registred_users": User.objects.filter(lazyuser__isnull=True).count(),
        "profiles": UserProfile.objects.all().count(),
        "children": User.objects.filter(username__startswith="child_").count(),

        "questions": Question.objects.filter(active=True).count(),
        "answers": Answer.objects.all().count(),
    })


def skills(request):

    selected_skill = None
    question = None

    if request.method == "POST":
        form = SelectSkillForm(request.POST)
        if "skill2" in request.POST and request.POST["skill2"]:
            selected_skill = request.POST["skill2"]
            form.fields["skill3"] = NoteModelChoiceField(queryset=Skill.objects.filter(parent=request.POST["skill2"]),
                                                             required=False,
                                                             widget=forms.Select(attrs={"onChange": "submit()"}))

            if "skill3" in request.POST and request.POST["skill3"]:
                selected_skill = request.POST["skill3"]
                form.fields["skill4"] = NoteModelChoiceField(queryset=Skill.objects.filter(parent=request.POST["skill3"]),
                                                             required=False,
                                                             widget=forms.Select(attrs={"onChange": "submit()"}))

                if "skill4" in request.POST and request.POST["skill4"]:
                    selected_skill = request.POST["skill4"]

        if "question" in request.POST and request.POST["question"]:
            question = Question.objects.get(pk=request.POST["question"])

    else:
        form = SelectSkillForm()

    if selected_skill:
        selected_skill = Skill.objects.get(pk=selected_skill)
    else:
        selected_skill = Skill.objects.get(level=1)

    selected_skill.questions_direct = Question.objects.filter(skill=selected_skill).count()
    selected_skill.questions = Question.objects.filter(skill__in=selected_skill.children_list.split(",")).count()
    selected_skill.answers = Answer.objects.filter(question__skill__pk__in=selected_skill.children_list.split(",")).count()
    selected_skill.user_skill = UserSkill.objects.filter(skill=selected_skill).aggregate(Avg("value"))["value__avg"]
    selected_skill.difficulty_direct = QuestionDifficulty.objects.filter(question__skill=selected_skill).aggregate(value=Avg("value"), time=Avg("time_intensity"))
    if selected_skill.difficulty_direct["time"]:
        selected_skill.difficulty_direct["time"] = e**selected_skill.difficulty_direct["time"]

    selected_skill.difficulty = QuestionDifficulty.objects.filter(question__skill__in=selected_skill.children_list.split(",")).aggregate(value=Avg("value"), time=Avg("time_intensity"))
    if selected_skill.difficulty["time"]:
        selected_skill.difficulty["time"] = e**selected_skill.difficulty["time"]

    form.fields["question"] = QuestionModelChoiceField(queryset=Question.objects.filter(skill=selected_skill).prefetch_related("player"),
                                                 required=False,
                                                 widget=forms.Select(attrs={"onChange": "submit()"}))

    if question:
        question.wrong_answers = Answer.objects.filter(correctly_solved=False, question=question).values("answer").annotate(Count("answer"))
        question.answer_count = Answer.objects.filter(question=question).count()
        question.correct_answer_count = Answer.objects.filter(question=question, correctly_solved=True).count()
        question.time = e**question.difficulty.time_intensity

        question.times = Answer.objects.filter(question=question).values("solving_time").annotate(Count("solving_time"))


    return render(request, 'administration/skills.html', {
            "form": form,
            "selected_skill": selected_skill,
            "question": question,
        })


class NoteModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.note

class QuestionModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{0} - {1}".format(obj.player, obj.data)

class SelectSkillForm(forms.Form):
    skill2 = NoteModelChoiceField(queryset=Skill.objects.filter(level=2).order_by("name"), required=True,
                                    widget=forms.Select(attrs={"onChange": "submit()"}))


def skill_tables(request):
    skills = {}
    for skill in Skill.objects.filter(level=4).annotate(difficulty=Avg("questions__difficulty__value")):
        skills[skill.name] = skill
        if skill.difficulty:
            skill.style = get_style(-skill.difficulty)

    return render(request, 'administration/skill_tables.html', {
        "skills4": skills,
        "skills2": Skill.objects.filter(level=2),
        "skill_tables": SKILL_TABLES,
        "names": NAMES,
    })

def skill_tables_counts(request):

    skills = {}
    max =  float(Skill.objects.filter(level=4).annotate(count=Count("questions__answers")).aggregate(max=Max("count"))["max"])
    for skill in Skill.objects.filter(level=4).annotate(count=Count("questions__answers")):
        skills[skill.name] = skill
        if skill.count:
            skill.style = get_style(- (skill.count / max * 6 - 3))

    return render(request, 'administration/skill_tables_counts.html', {
        "skills4": skills,
        "skills2": Skill.objects.filter(level=2),
        "skill_tables": SKILL_TABLES,
        "names": NAMES,
        })

NAMES = ('numbers', 'addition', 'subtraction', 'multiplication', 'division')
SKILL_TABLES = {
    'numbers':
        [[str(c + r * 10) for c in range(1, 11)] for r in range(2)],
    'addition':
        [['%s+%s' % (c, r) for c in range(1, r) if c + r <= 20] for r in range(1, 21)],
    'subtraction':
        [['%s-%s' % (r, c) for c in range(1, r + 1)] for r in range(1, 11)],
    'multiplication':
        [['%sx%s' % (c, r) for c in range(1, 11) if r >= c] for r in range(1, 21)],
    'division':
        [['%s/%s' % (a * b, b) for a in range(1, 11)] for b in range(1, 11)],
    }