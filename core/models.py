from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from lazysignup.utils import is_lazy_user


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    children = models.ManyToManyField('self', related_name="supervisors", symmetrical=False)

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

@receiver(user_logged_in)
def after_log_in(sender, **kwargs):
    if "user" in kwargs:    # user logged in - check profile
        create_profile(kwargs["user"])


def create_profile(user):
    if not hasattr(user, "profile") and is_user_registred(user):
        profile = UserProfile(user=user)
        profile.save()
        return profile