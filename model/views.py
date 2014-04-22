from django.shortcuts import render
from lazysignup.decorators import allow_lazy_user
from model.models import UserSkill, Skill


@allow_lazy_user
def my_skills(request):
    skills = set()
    for s in Skill.objects.\
            filter(parent__name__in=['addition <= 10', 'addition <= 20',
                                     'numbers <= 10', 'numbers <= 20',
                                     'numbers <= 100']):
        skills.add(s.name)
    user_skills = {k: None for k in skills}
    for us in UserSkill.objects.filter(user=request.user):
        user_skills[us.skill.name] = us.value

    tables = []
    tables.append([[get_skill_repr(str(c + r * 10), user_skills)
                    for c in range(1, 11)] for r in range(10)])
    tables.append([[get_skill_repr('%s+%s' % (c, r), user_skills)
                    for c in range(1, 11)] for r in range(1, 21)])

    return render(request, 'model/my_skills.html', {
        "tables": tables,
    })


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
