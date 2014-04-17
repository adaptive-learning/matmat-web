from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Skill(models.Model):
    name = models.CharField(max_length=30)
    note = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("model.Skill", null=True, blank=True,
                               related_name="children")
    level = models.IntegerField()

    def __unicode__(self):
        return self.name

    def get_children(self):
        # using DFS to aviod infinite loops in case child is also a parent
        fringe = [self]
        children = set([self])

        while fringe:
            node = fringe.pop(0)
            if node.level < 4:
                for ch in node.children.all():
                    if ch not in children:
                        fringe.append(ch)
                        children.add(ch)

        return list(children)


@receiver(pre_save, sender=Skill)
def compute_level(sender, instance, **kwargs):
    if instance.parent is None:
        instance.level = 1
    else:
        instance.level = instance.parent.level + 1


class QuestionDifficulty(models.Model):
    question = models.OneToOneField('questions.Question', primary_key=True,
                                    related_name='difficulty')
    value = models.FloatField(default=0)

    def __unicode__(self):
        return self.value

    def get_first_attempts_count(self):
        return self.question.answers.values('user').distinct().count()


class UserSkill(models.Model):
    user = models.ForeignKey(User)
    skill = models.ForeignKey(Skill)
    value = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'skill')
