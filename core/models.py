from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    children = models.ManyToManyField('self', related_name="supervisors")


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    instance = kwargs["instance"]
    created = kwargs["created"]
    if created:
        profile = UserProfile(user=instance)
        profile.save()