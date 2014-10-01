from collections import defaultdict
from django.db import connection
from django.shortcuts import render
from lazysignup.decorators import allow_lazy_user
import colorsys
import math
from collections import namedtuple


NAMES = ('numbers', 'addition', 'subtraction', 'multiplication', 'division')
SKILL_TABLES = {
    'numbers':
    [[str(c + r * 10) for c in range(1, 11)] for r in range(2)],
    'addition':
    [['%s+%s' % (c, r) for c in range(1, 11)] for r in range(1, 21)],
    'subtraction':
    [['%s-%s' % (r, c) for c in range(1, r + 1)] for r in range(1, 11)],
    'multiplication':
    [['%sx%s' % (c, r) for c in range(1, 11)] for r in range(1, 21)],
    'division':
    [['%s/%s' % (a * b, b) for a in range(1, 11)] for b in range(1, 11)],
}

skill_keys = ['pk', 'name', 'note', 'value', 'value_percent', 'style', 'image_name']
SkillTuple = namedtuple('Skill', ', '.join(skill_keys))
skill_as_tuple = lambda skill: SkillTuple(*[skill[k] for k in skill_keys])


@allow_lazy_user
def my_skills(request, pk=None):
    all_skills = get_all_skills(request.user)

    par = None
    while pk is not None:
        par, pk = pk, all_skills['id_parid'][pk]
    active = all_skills['id_name'][par] if par is not None else 'numbers'

    data = []
    skills = []
    for name in NAMES:
        skill = get_skill_obj_by_name(name, all_skills)
        skills.append(skill)
        data.append(get_my_skills(name, all_skills))
        print skill

    ret = render(request, 'model/my_skills.html', {
        "data": data,
        "skills": skills,
        "active": active,
    })

    return ret


def get_all_skills(user):
    cursor = connection.cursor()
    cursor.execute(
        '''SELECT s.id, s.parent_id, s.name, usk.val, s.note
        FROM model_skill s LEFT JOIN
            (SELECT us.skill_id as sid, us.value as val
             FROM model_userskill us
             WHERE us.user_id={0}) usk
        ON (s.id = usk.sid)
        '''.format(user.pk))
    rows = cursor.fetchall()
    skills = {sid: (parid, name, val, note)
              for sid, parid, name, val, note in rows}
    user_skills = {}
    name_id = {}
    id_name = {}
    id_parid = {}
    id_note = {}
    id_used = {}
    children = defaultdict(list)
    for sid, (parid, name, val, note) in skills.iteritems():
        get_skill_value(sid, skills, user_skills)
        name_id[name] = sid
        id_name[sid] = name
        id_parid[sid] = parid
        id_note[sid] = note
        id_used[sid] = val is not None
        if parid:
            children[parid].append(sid)
    return {'name_id': name_id,
            'id_name': id_name,
            'id_val': user_skills,
            'id_parid': id_parid,
            'children': children,
            'id_note': id_note,
            'id_used': id_used,
            }


def get_children(parent_list, skills):
    parids = [skills['name_id'][p] for p in parent_list]
    children = [ch for parid in parids for ch in skills['children'][parid]]
    ret = {}
    for sid in children:
        obj = get_skill_obj(sid, skills)
        ret[obj.name] = obj
    return ret


def get_skill_obj(sid, skills):
    obj = {'name': skills['id_name'][sid],
           'value': skills['id_val'][sid],
           'image_name': "core/imgs/skill_{}.png".format(skills['id_name'][sid]),
           'pk': sid,
           'note': skills['id_note'][sid],
           'used': skills['id_used'][sid]}
    obj['value_percent'] = int(100. / (1 + math.exp(-obj['value'])))
    obj['style'] = get_style(obj['value'], used=skills['id_used'][sid])
    return skill_as_tuple(obj)


def get_skill_value(sid, skills, user_skills):
    """
    compute and save absolute skill of user
    """
    if sid not in user_skills:
        parid, name, val, _ = skills[sid]
        val = val or 0
        parval = get_skill_value(parid, skills, user_skills) if parid else 0
        user_skills[sid] = val + parval
    return user_skills[sid]


def get_skill_obj_by_name(name, skills):
    sid = skills['name_id'][name]
    return get_skill_obj(sid, skills)


def get_my_skills(name, skills):
    top = get_children([name], skills)
    children = get_children([s.name for s in top.values()], skills)
    return {
        "table": [[get_skill_repr(c, children) for c in r]
                  for r in SKILL_TABLES[name]],
        "skills": top,
        "skill": get_skill_obj_by_name(name, skills),
    }


def get_skill_repr(name, user_skills):
    if name in user_skills:
        return {'name': name, 'style': user_skills[name].style}
    else:
        return {'name': '', 'style': get_style(None)}


def get_style(value, used=True):
    ''' return css style of user skill'''
    if value is None:
        return 'background-color: rgba(127, 127, 0, 0);'

    value = (1 / (1 + math.exp(-value)))
    color = colorsys.hsv_to_rgb(1. / 12 + value * 2 / 9., 1, 0.8)
    color = [int(c * 255) for c in color]
    alpha = 1 if used else 0.2
    return "background-color: rgba({0[0]}, {0[1]}, {0[2]}, {1});".\
        format(color, alpha)
