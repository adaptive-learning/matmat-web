from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from lazysignup.models import LazyUser
from lazysignup.utils import is_lazy_user
from social_auth.db.django_models import UserSocialAuth


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
        profile.save()
        return profile