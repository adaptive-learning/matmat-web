# coding=utf-8
import json
import string
from django.contrib import messages
from django.contrib.auth import user_logged_in, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.views.generic import View
from lazysignup.utils import is_lazy_user
from core.decorators import non_lazy_required
from core.models import create_profile, is_user_registred, convert_lazy_user, UserProfile
from matmat import settings
from model.models import Skill


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


def generate_random_string(lenght):
    import random
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(lenght))


class SupervisorOverviewView(View):
    def post(self, request, child_pk=None):
        child_form = ChildForm(request.POST)
        if child_form.is_valid():
            name = child_form.cleaned_data["name"]
            if child_pk is None:
                rand = generate_random_string(15)
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
            "children": request.user.profile.children.all(),
            })

supervisor_overview = non_lazy_required(SupervisorOverviewView.as_view())

@non_lazy_required
def log_as_child(request, child_pk):
    child = request.user.profile.children.get(user__pk=child_pk).user
    child.backend = 'django.contrib.auth.backends.ModelBackend'
    print login(request, child)
    return redirect("home")


class SendChildView(View):
    def post(self, request):
        if "email" in request.POST and "pk" in request.POST:
            child = UserProfile.objects.filter(pk=request.POST["pk"], supervisors=request.user.profile).first()
            if child:
                subject = u"MatMat - správa dítěte"
                from_email = settings.EMAIL_SELF
                to = request.POST["email"]
                data = {
                    "child": child,
                    "user": request.user,
                    "msg": request.POST["msg"],
                    "domain": request.build_absolute_uri(reverse("home"))[:-1]
                }
                text_content = render_to_string("emails/send_child.plain", data)
                html_content = render_to_string("emails/send_child.html", data)

                msg = EmailMultiAlternatives(subject, text_content, "MatMat <{}>".format(from_email), [to])
                if request.user.email:
                    msg.extra_headers = {'Reply-To': request.user.email}
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                messages.success(request, "Email úspěšně odeslán")
                return redirect("supervisor_overview")

        messages.error(request, "Bohuželo došlo k chybě")
        return redirect("supervisor_overview")

send_child = non_lazy_required(SendChildView.as_view())


@non_lazy_required
def receive_child(request, code):
    child = UserProfile.objects.filter(code=code).first()
    if child is None:
        messages.error(request, "Bohuželo došlo k chybě při přidávání dítěte")
        return redirect("supervisor_overview")

    request.user.profile.children.add(child)

    messages.success(request, "Dítě úspěšně přidáno")

    return redirect("supervisor_overview")



def feedback(request):
    msg = "Někde se stala chyba"
    if request.method == "POST":
        data = json.loads(request.body)

        subject = u"MatMat - feedback"
        from_email = settings.EMAIL_SELF
        to = settings.EMAIL_CONTACT
        text_content = render_to_string("emails/feedback.plain", {
            "data": data,
            "user": request.user,
        })
        html_content = render_to_string("emails/feedback.html", {
            "data": data,
            "user": request.user,
        })

        msg = EmailMultiAlternatives(subject, text_content, "MatMat <{}>".format(from_email), [to])
        if "email" in data:
            msg.extra_headers = {'Reply-To': data["email"]}
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        msg = "Úspěšně odesláno. Děkujeme!"


    return HttpResponse(json.dumps({
        "msg": msg,
        }), content_type="application/json")


def ajax_login(request):
    context = {}
    if request.method == "POST":
        body = json.loads(request.body)
        user = None
        if 'username' in body and 'password' in body:
            username = body['username']
            password = body['password']
            user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                context['success'] = True
            else:
                context['success'] = False
                context['error_msg'] = 'Uživatelský účet není aktviní.'
        else:
            context['success'] = False
            context['error_msg'] = 'Špatné jméno nebo heslo'

    return HttpResponse(json.dumps(context), content_type="application/json")
