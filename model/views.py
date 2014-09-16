from django.shortcuts import render
from lazysignup.decorators import allow_lazy_user
import math
from model.models import UserSkill, Skill

user_skills_cache = {}
@allow_lazy_user
def my_skills(request):
    data = {}
    skills = []
    for name, getter in zip(NAMES, GETTERS):
        skill = Skill.objects.get(name=name)
        data[skill] = getter(request.user)
        skills.append(skill)

    user_skills_cache = {}

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
        us.value = us.value + get_user_skill_value(user, us.skill.parent_id)   # compute skill from parents
        us.value_percent = int(100. / (1 + math.exp(-us.value)))
    return user_skills


def get_user_skill_by_name(name, user):
    user_skill = UserSkill.objects.filter(user=user, skill__name=name)
    if len(user_skill) == 1:
        user_skill = user_skill[0]
        user_skill.value = user_skill.value + get_user_skill_value(user, user_skill.skill.parent_id)   # compute skill from parents
        user_skill.value_percent = int(100. / (1 + math.exp(-user_skill.value)))
    else:
        user_skill = None

    return user_skill

def get_user_skill_value(user, skill):
    """
    compute absolute skill of user
    """
    # look to the cache
    if "{0}-{1}".format(user.pk, skill) in user_skills_cache.keys():
        return user_skills_cache["{0}-{1}".format(user.pk, skill)]

    skill = Skill.objects.get(pk=skill)
    user_skill = UserSkill.objects.get(user=user, skill=skill)

    # stop recursion on root
    if skill.parent is None:
        if user_skill is None:
            return 0
        else:
            return user_skill.value

    # initialize skill if does not exist
    if user_skill is None:
        user_skill = 0

    parent_user_skill_value = get_user_skill_value(user, skill.parent_id)
    user_skills_cache["{0}-{1}".format(user.pk, skill.pk)] = user_skill.value + parent_user_skill_value
    return user_skill.value + parent_user_skill_value

def my_skills_numbers(user):
    user_skills = get_user_skills(user, ['numbers <= 10', 'numbers <= 20',
                                         'numbers <= 100'])

    return {
        "table": [[get_skill_repr(str(c + r * 10), user_skills)
                   for c in range(1, 11)] for r in range(10)],
        "skills": get_user_skills(user, ["numbers"]),
        "skill": get_user_skill_by_name("numbers", user),
    }


def my_skills_addition(user):
    user_skills = get_user_skills(user, ['addition <= 10', 'addition <= 20'])
    return {
        "table": [[get_skill_repr('%s+%s' % (c, r), user_skills)
                   for c in range(1, 11)] for r in range(1, 21)],
        "skills": get_user_skills(user, ["addition"]),
        "skill": get_user_skill_by_name("addition", user),
    }


def my_skills_multiplication(user):
    user_skills = get_user_skills(user, ['multiplication1', 'multiplication2'])
    return {
        "table": [[get_skill_repr('%sx%s' % (c, r), user_skills)
                   for c in range(11)] for r in range(21)],
        "skills": get_user_skills(user, ["multiplication"]),
        "skill": get_user_skill_by_name("multiplication", user),
    }


def my_skills_division(user):
    user_skills = get_user_skills(user, ['division1'])
    return {
        "table": [[get_skill_repr('%s/%s' % (a * b, b), user_skills)
             for a in range(11)] for b in range(1, 11)],
        "skills": get_user_skills(user, ["division"]),
        "skill": get_user_skill_by_name("division", user),
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
