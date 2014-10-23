# coding=utf-8
import string
from django.contrib.auth import user_logged_in, login
from django.contrib.auth.models import User
from django.dispatch import receiver
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from lazysignup.decorators import allow_lazy_user
from lazysignup.utils import is_lazy_user
from core.decorators import non_lazy_required
from core.models import create_profile, is_user_registred, convert_lazy_user
from model.models import Skill


@allow_lazy_user
def home(request):
    request.session.set_expiry(0)
    order = [u"math", u"numbers", u"addition", u"subtraction",
             u"multiplication", u"division"]
    skills = list(Skill.objects.filter(level__in=[1, 2]))
    skills.sort(key=lambda s: order.index(s.name))

    remember_user(request)
    if is_lazy_user(request.user) and is_user_registred(request.user):
        convert_lazy_user(request.user)

    return render(request, 'core/home.html', {
        "skills": skills,
    })


@receiver(user_logged_in)
def remember_user(request, **kwargs):
    """
    'remember me' after log in
    """
    request.session.set_expiry(0)


class ChildForm(forms.Form):
    name = forms.CharField(max_length=50, label="Jméno")


class SupervisorOverviewView(View):
    def post(self, request, child_pk=None):
        child_form = ChildForm(request.POST)
        if child_form.is_valid():
            name = child_form.cleaned_data["name"]
            if child_pk is None:
                import random
                rand = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
                username = "child_" + rand
                child = User(username=username, first_name=name)
                child.save()
                create_profile(child)
                request.user.profile.children.add(child.profile)
            else:
                child = request.user.profile.children.get(user__pk=child_pk)
                child.user.first_name = name
                child.user.save()

            return redirect("supervisor_overview")

        return render(request, 'core/supervisor_overview.html', {
            "child_form": child_form,
            "child_pk": child_pk,
        })


    def get(self, request, child_pk=None):
        child_form = ChildForm()
        if child_pk is not None:
            child = get_object_or_404(User, pk=child_pk)
            child_form.fields["name"].initial = child.first_name

        return render(request, 'core/supervisor_overview.html', {
            "child_form": child_form,
            "child_pk": child_pk,
            })

supervisor_overview = non_lazy_required(SupervisorOverviewView.as_view())

@non_lazy_required
def log_as_child(request, child_pk):
    child = request.user.profile.children.get(user__pk=child_pk).user
    child.backend = 'django.contrib.auth.backends.ModelBackend'
    print login(request, child)
    return redirect("home")
