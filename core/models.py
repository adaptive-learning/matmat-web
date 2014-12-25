# coding=utf-8
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from lazysignup.forms import UserCreationForm
from lazysignup.models import LazyUser
from lazysignup.utils import is_lazy_user
from social_auth.db.django_models import UserSocialAuth
from core.utils import generate_random_string


class NameUserCreationForm(UserCreationForm):

    first_name = forms.CharField(label=u"Zobrazované jméno", max_length=30)
    email = forms.EmailField(label=u"E-mail", required=False, widget=forms.TextInput(attrs={"placeholder": "nepovinné"}))

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "email")


class UserProfile(models.Model):
    PLAIN = "pl"
    WIZARD = "wi"
    GRAPHICS = (
        (PLAIN, "prostý"),
        (WIZARD, "kouzelník")
    )

    user = models.OneToOneField(User, related_name="profile")
    children = models.ManyToManyField('self', related_name="supervisors", symmetrical=False)
    code = models.CharField(max_length=10)
    graphics = models.CharField(max_length=2, choices=GRAPHICS, default=WIZARD)

    def is_child(self):
        return self.supervisors.exists()

    def has_children(self):
        return self.children.exists()


def is_user_registred(user):
    if not user.is_authenticated() or user.is_anonymous():
        return False
    if user.social_auth.exists():
        return True
    return not is_lazy_user(user)


def convert_lazy_user(user):
    if LazyUser.objects.filter(user=user).count() == 0:
        return
    LazyUser.objects.get(user=user.pk).delete()
    user.username = user.first_name + " " + user.last_name
    user.save()

@receiver(user_logged_in)
def after_log_in(sender, **kwargs):
    if "user" in kwargs:    # user logged in - check profile
        create_profile(kwargs["user"])


@receiver(post_save, sender=UserSocialAuth)
def my_handler(sender, instance, created=False, **kwargs):
    create_profile(instance.user)


def create_profile(user):
    if not hasattr(user, "profile") and is_user_registred(user):
        profile = UserProfile(user=user)
        profile.code = generate_random_string(10)
        profile.save()
        return profile