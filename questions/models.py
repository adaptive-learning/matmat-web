from django.contrib.auth.models import User
from django.db import models


class Simulator(models.Model):
    name = models.CharField(max_length=30)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    TYPES = (
        ('t', 'time'),
        ('c', 'correctness')
    )

    player = models.ForeignKey(Simulator, verbose_name="Simulator")
    skill = models.ForeignKey('model.Skill')
    data = models.TextField(verbose_name="Data as JSON")
    type = models.CharField(max_length=1, choices=TYPES, default='c')
    value = models.CharField(max_length=255, null=True, blank=True)     # value for preventing repeating similar questions

    def __unicode__(self):
        return self.data

    def as_json(self):
        return dict(
            pk=self.pk,
            data=self.data,
            simulator=self.player.name,
            recommendation_log=self.recommendation_log if hasattr(self, "recommendation_log") else None
        )


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    user = models.ForeignKey(User)
    log = models.TextField()
    solving_time = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    correctly_solved = models.BooleanField(default=False)

    def is_first_attempt(self):
        return Answer.objects.filter(user=self.user, question=self.question, timestamp__lt=self.timestamp).count() == 0