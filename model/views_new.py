from django.shortcuts import render, get_object_or_404
from model.models import Skill

BASE_SKILLS = ['numbers', 'addition', 'subtraction', 'multiplication', 'division']

def my_skills(request, proceed_skill=None):

    active = None
    if proceed_skill is not None:
        proceed_skill = get_object_or_404(Skill, pk=proceed_skill, level__lte=3)
        active = proceed_skill.parent_list()[-2].name if proceed_skill.level > 2 \
            else proceed_skill.name if proceed_skill.level == 2 else BASE_SKILLS[0]
        print active, proceed_skill.parent_list()

    return render(request, "model/my_skills_new.html", {
        "active": active if active is not None else BASE_SKILLS[0],
        "proceed_skill": proceed_skill,
        "skills": sorted(Skill.objects.filter(name__in=BASE_SKILLS), key=lambda s: BASE_SKILLS.index(s.name)),
        "image_names": {skill.name: skill.get_image_name(request.user) for skill in Skill.objects.filter(level=2)},
    })