from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model.models import Skill


class Player(models.Model):
    name = models.CharField(max_length=30)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

# @receiver(post_save, sender=Player)
# def create_dir_for_player(sender, instance, **kwargs):
#     pass


class Question(models.Model):
    player = models.ForeignKey(Player)
    skill = models.ForeignKey(Skill)
    data = models.TextField()

    def __unicode__(self):
        return self.data
