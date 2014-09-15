from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from django.shortcuts import render
from lazysignup.decorators import allow_lazy_user
from model.models import Skill


@allow_lazy_user
def home(request):
    order = [u"math", u"numbers", u"addition", u"subtraction",
             u"multiplication", u"division"]
    skills = list(Skill.objects.filter(level__in=[1, 2]))
    skills.sort(key=lambda s: order.index(s.name))

    return render(request, 'core/home.html', {
        "skills": skills,
    })


@receiver(user_logged_in)
def remember_user(request, **kwargs):
    request.session.set_expiry(0)
