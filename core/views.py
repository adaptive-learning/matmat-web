from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from django.shortcuts import render
from lazysignup.decorators import allow_lazy_user
from model.models import Skill


@allow_lazy_user
def home(request):
    return render(request, 'core/home.html', {
        "skills": Skill.objects.filter(level=2)
    })

@receiver(user_logged_in)
def remember_user(request, **kwargs):
    request.session.set_expiry(0)