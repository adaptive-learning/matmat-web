import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from lazysignup.decorators import allow_lazy_user
from core.decorators import non_lazy_required
from model.models import Skill, UserSkill
from questions.management.commands.generate_questions import BASE_SKILLS, SUB_SKILLS, SKILL_TABLES


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
        "user_showed": user if user_pk is not None else None,
        "data": json.dumps({
            "active": active if active is not None else [BASE_SKILLS[0]],
            "user_diffs": dict(UserSkill.objects.all_diffs(user)),
            "user_skills": UserSkill.objects.all_skills(user),
            "base_skills": BASE_SKILLS,
            "sub_skills": SUB_SKILLS,
            "skill_tables": SKILL_TABLES,
            "skills": skills,
            "proceed_skill": proceed_skill.name if proceed_skill is not None else "",
        }),
    })


@non_lazy_required
def children_comparison(request):
    user = request.user

    return render(request, "model/children_comparison.html", {
        "data": get_data_for_children_comparison(user)
    })


def get_data_for_children_comparison(user):
    children = user.profile.children.all().order_by("user__last_name", "user__first_name").select_related("user")

    skill_objects = Skill.objects.filter(level__lt=4, active=True)
    skills = {child.user.pk: dict(map(lambda s: (s.name, s.to_json(user, details=False)), skill_objects)) for child in children}

    return json.dumps({
        "user_diffs": {child.user.pk: dict(UserSkill.objects.all_diffs(child.user)) for child in children},
        "user_skills": {child.user.pk: UserSkill.objects.all_skills(child.user) for child in children},
        "answer_counts": Skill.objects.answer_counts([c.user for c in children], skill_objects),
        "answer_correct_counts": Skill.objects.answer_counts([c.user for c in children], skill_objects, correctly_solved=True),
        "base_skills": BASE_SKILLS,
        "sub_skills": SUB_SKILLS,
        "skills": skills,
        "children": {child.user.pk: child.to_json() for child in children},
        "children_ids": [child.user.pk for child in children],
    })


@non_lazy_required
def skill_detail(request, user_pk, skill_pk):
    try:
        user = request.user.profile.children.get(user__id=user_pk).user
    except:
        return HttpResponseNotFound("User not found")
    skill = get_object_or_404(Skill, pk=skill_pk)
    return JsonResponse(skill.to_json(user))