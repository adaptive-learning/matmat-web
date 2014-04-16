from django.shortcuts import render
from lazysignup.decorators import allow_lazy_user
from model.models import Skill


@allow_lazy_user
def home(request):
    return render(request, 'core/home.html', {
        "skills": Skill.objects.filter(level=2)
    })