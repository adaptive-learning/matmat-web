from django.shortcuts import render
from lazysignup.decorators import allow_lazy_user
import math
from model.models import UserSkill, Skill


@allow_lazy_user
def my_skills(request):
    data = {}
    skills = []
    for name, getter in zip(NAMES, GETTERS):
        skill = Skill.objects.get(name=name)
        data[skill] = getter(request.user)
        skills.append(skill)

    return render(request, 'model/my_skills.html', {
        "data": data,
        "skills": skills,
        "active": "numbers",
    })


def get_user_skills(user, parent_list):
    skills = Skill.objects.filter(parent__name__in=parent_list)
    skills_name = set([s.name for s in skills])
    user_skills = {k: None for k in skills_name}
    for us in UserSkill.objects.filter(user=user.pk, skill__in=skills)\
            .select_related("skill"):
        user_skills[us.skill.name] = us
        us.value_percent = int(100. / (1 + math.exp(-us.value)))
    return user_skills


def get_user_skill(name, user):
    skill = UserSkill.objects.filter(user=user, skill__name=name)
    if len(skill) == 1:
        skill = skill[0]
        skill.value_percent = int(100. / (1 + math.exp(-skill.value)))
    else:
        skill = None

    return skill


def my_skills_numbers(user):
    user_skills = get_user_skills(user, ['numbers <= 10', 'numbers <= 20',
                                         'numbers <= 100'])

    return {
        "table": [[get_skill_repr(str(c + r * 10), user_skills)
                   for c in range(1, 11)] for r in range(10)],
        "skills": get_user_skills(user, ["numbers"]),
        "skill": get_user_skill("numbers", user),
    }


def my_skills_addition(user):
    user_skills = get_user_skills(user, ['addition <= 10', 'addition <= 20'])
    return {
        "table": [[get_skill_repr('%s+%s' % (c, r), user_skills)
                   for c in range(1, 11)] for r in range(1, 21)],
        "skills": get_user_skills(user, ["addition"]),
        "skill": get_user_skill("addition", user),
    }


def my_skills_multiplication(user):
    user_skills = get_user_skills(user, ['multiplication1', 'multiplication2'])
    return {
        "table": [[get_skill_repr('%sx%s' % (c, r), user_skills)
                   for c in range(11)] for r in range(21)],
        "skills": get_user_skills(user, ["addition"]),
        "skill": get_user_skill("multiplication", user),
    }


def my_skills_division(user):
    user_skills = get_user_skills(user, ['division1'])
    return {
        "table": [[get_skill_repr('%s/%s' % (a * b, b), user_skills)
                   for a in range(11)] for b in range(1, 11)],
        "skills": get_user_skills(user, ["division"]),
        "skill": get_user_skill("division", user),
    }


def get_skill_repr(name, user_skills):
    if name in user_skills:
        return {'name': name, 'style': get_style(user_skills[name])}
    else:
        return {'name': '', 'style': get_style(None)}


def get_style(user_skill):
    ''' for now scale values from -5 to +5'''
    if user_skill is None:
        return 'background-color: rgba(127, 127, 127, 0);'
    value = user_skill.value
    if value >= 0:
        value = min(value, 5)
        return 'background-color: rgba(44, 160, 44, %.2f);' % (value / 5.)
    if value < 0:
        value = max(value, -5)
        return 'background-color: rgba(214, 39, 40, %.2f);' % (-value / 5.)


NAMES = ('numbers', 'addition', 'multiplication', 'division')
GETTERS = (my_skills_numbers, my_skills_addition,
           my_skills_multiplication, my_skills_division)
