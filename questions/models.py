from django.contrib.auth.models import User
from django.db import models
from model.models import Skill


class Simulator(models.Model):
    TYPES = (
        ('t', 'time'),
        ('c', 'correctness')
    )

    name = models.CharField(max_length=30)
    note = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=1, choices=TYPES, default='t')

    def __unicode__(self):
        return self.name


class Question(models.Model):
    player = models.ForeignKey(Simulator)
    skill = models.ForeignKey(Skill)
    data = models.TextField(verbose_name="Data as JSON")

    def __unicode__(self):
        return self.data

    def as_json(self):
        return dict(
            pk=self.pk,
            data=self.data,
            simulator=self.player.name,
        )


class Answer(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    log = models.TextField()
    solving_time = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)