from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    children = models.ManyToManyField('self', related_name="supervisors")

def is_user_logged(user):
    return user.social_auth.exists()

@receiver(user_logged_in)
def after_log_in(sender, **kwargs):
    if "user" in kwargs:    # user logged in - check profile
        create_profile(kwargs["user"])


@receiver(post_save, sender=User)
def post_user_save(sender, **kwargs):
    user = kwargs["instance"]
    create_profile(user)


def create_profile(user):
    if not hasattr(user, "profile") and is_user_logged(user):
        profile = UserProfile(user=user)
        profile.save()