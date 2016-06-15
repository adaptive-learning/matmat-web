import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from proso_models.models import get_environment, get_predictive_model
from proso_tasks.models import Skill

from matmat import settings
from matmat.skills import SKILL_TABLES


def index(request):
    return render(request, "index.html", {
        "user": json.dumps(request.user.userprofile.to_json()) if hasattr(request.user, "userprofile") else "",
        "DEBUG": settings.DEBUG,
        "GOOGLE_ANALYTICS": settings.ON_SERVER,
    })


def small_concepts(request, skill_identifier):
    if skill_identifier not in SKILL_TABLES:
        return JsonResponse({'msg': 'no_table'})
    skill = get_object_or_404(Skill, identifier=skill_identifier)

    skills = Skill.objects.filter(item__child_relations__parent=skill.item_id, active=True)
    items = [s.item_id for s in skills]
    environment = get_environment()
    model = get_predictive_model()
    predictions = model.predict_more_items(environment, request.user.pk, items, datetime.now())
    answer_counts = environment.read_more_items('answer_count', user=request.user.pk, items=items, default=0)

    data = {}
    for s, p, a in zip(skills, predictions, answer_counts):
        data[s.identifier] = {
            'name': s.name,
            'prediction':p,
            'answer_count': a
        }

    return JsonResponse({
        'structure': SKILL_TABLES[skill_identifier],
        'data': data
    })