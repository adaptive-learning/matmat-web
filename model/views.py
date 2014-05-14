from django.shortcuts import render
from lazysignup.decorators import allow_lazy_user
from model.models import UserSkill, Skill


@allow_lazy_user
def my_skills(request):
    data = {}
    skills = []
    for name, getter in zip(NAMES, GETTERS):
        skill = Skill.objects.get(name=name)
        data[skill] = {'table': getter(request.user)}
        skills.append(skill)

    return render(request, 'model/my_skills.html', {
        "data": data,
        "skills": skills,
        "active": "numbers",
    })


def get_user_skills(user, parent_list):
    skills = set([s.name for s in Skill.objects.
                  filter(parent__name__in=parent_list)])
    user_skills = {k: None for k in skills}
    for us in UserSkill.objects.filter(user=user):
        user_skills[us.skill.name] = us.value
    return user_skills


def my_skills_numbers(user):
    user_skills = get_user_skills(user, ['numbers <= 10', 'numbers <= 20',
                                         'numbers <= 100'])
    return [[get_skill_repr(str(c + r * 10), user_skills)
             for c in range(1, 11)] for r in range(10)]


def my_skills_addition(user):
    user_skills = get_user_skills(user, ['addition <= 10', 'addition <= 20'])
    return [[get_skill_repr('%s+%s' % (c, r), user_skills)
             for c in range(1, 11)] for r in range(1, 21)]


def my_skills_multiplication(user):
    user_skills = get_user_skills(user, ['multiplication1', 'multiplication2'])
    return [[get_skill_repr('%sx%s' % (c, r), user_skills)
             for c in range(11)] for r in range(21)]


def my_skills_fractions(user):
    user_skills = get_user_skills(user, ['division1'])
    return [[get_skill_repr('%s/%s' % (a * b, b), user_skills)
             for a in range(11)] for b in range(1, 11)]


def get_skill_repr(name, user_skills):
    if name in user_skills:
        return {'name': name, 'style': get_style(user_skills[name])}
    else:
        return {'name': '', 'style': get_style(None)}


def get_style(value):
    ''' for now scale values from -5 to +5'''
    if value is None:
        return 'background-color: rgba(127, 127, 127, 0);'
    if value >= 0:
        value = min(value, 5)
        return 'background-color: rgba(44, 160, 44, %.2f);' % (value / 5.)
    if value < 0:
        value = max(value, -5)
        return 'background-color: rgba(214, 39, 40, %.2f);' % (-value / 5.)


NAMES = ('numbers', 'addition', 'multiplication', 'fractions')
GETTERS = (my_skills_numbers, my_skills_addition,
           my_skills_multiplication, my_skills_fractions)
