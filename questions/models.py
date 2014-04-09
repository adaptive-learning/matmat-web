import json
from django.db import models
from model.models import Skill


class Simulator(models.Model):
    name = models.CharField(max_length=30)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

# @receiver(post_save, sender=Player)
# def create_dir_for_player(sender, instance, **kwargs):
#     pass


class Question(models.Model):
    player = models.ForeignKey(Simulator)
    skill = models.ForeignKey(Skill)
    data = models.TextField(verbose_name="Data as JSON")

    def __unicode__(self):
        return self.data

    def as_json(self):
        return dict(
            pk=self.pk,
            # data=json.loads(self.data),
            data=self.data,
            simulator=self.player.name,
        )
