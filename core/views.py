from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from django.shortcuts import render
from lazysignup.decorators import allow_lazy_user
from model.models import Skill


@allow_lazy_user
def home(request):
    def order(skill):
        skill_names = [u"numbers", u"addition", u"multiplication", u"division"]
        for index, name in enumerate(skill_names):
            if skill.name == name:
                return index

    skills = list(Skill.objects.filter(level=2))
    skills.sort(key=order)

    return render(request, 'core/home.html', {
        "skills": skills,
    })

@receiver(user_logged_in)
def remember_user(request, **kwargs):
    request.session.set_expiry(0)
