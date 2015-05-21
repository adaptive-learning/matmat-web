import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from lazysignup.decorators import allow_lazy_user
from model.models import Skill, UserSkill
from questions.management.commands.generate_questions import BASE_SKILLS, SUB_SKILL, SKILL_TABLES


@allow_lazy_user
@login_required
def my_skills(request, proceed_skill=None, user_pk=None):

    active = None
    if proceed_skill is not None:
        proceed_skill = get_object_or_404(Skill, pk=proceed_skill, level__lte=3)
        active = map(lambda p: p.name, proceed_skill.parent_list()[:-1]) + [proceed_skill.name] if proceed_skill.level > 2 \
            else [proceed_skill.name] if proceed_skill.level == 2 else [BASE_SKILLS[0]]

    user = request.user
    if user_pk:
        if request.user.is_superuser:
            user = get_object_or_404(User, pk=user_pk)
        else:
            user = get_object_or_404(User, pk=user_pk, profile__supervisors=request.user.profile)
        user.as_child = True

    skills = dict(map(lambda s: (s.name, s.to_json(user)), Skill.objects.filter(active=True)))

    return render(request, "model/my_skills.html", {
        "user_showed": user,
        "data": json.dumps({
            "active": active if active is not None else [BASE_SKILLS[0]],
            "user_diffs": dict(UserSkill.objects.all_diffs(user)),
            "user_skills": UserSkill.objects.all_skills(user),
            "base_skills": BASE_SKILLS,
            "sub_skills": SUB_SKILL,
            "skill_tables": SKILL_TABLES,
            "skills": skills,
            "proceed_skill": proceed_skill.name if proceed_skill is not None else "",
        }),
    })