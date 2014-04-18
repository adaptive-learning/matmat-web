from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver


class Skill(models.Model):
    name = models.CharField(max_length=30)
    note = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="children")
    level = models.IntegerField()
    children_list = models.TextField(default="")

    def __unicode__(self):
        return self.name


@receiver(pre_save, sender=Skill)
def compute_level(sender, instance, **kwargs):
    if instance.parent is None:
        instance.level = 1
    else:
        instance.level = instance.parent.level + 1

@receiver(pre_save, sender=Skill)
def check_cycles(sender, instance, **kwargs):
    list = []
    s = instance
    while s is not None:
        if s.pk in list:
            raise ValueError("Cycle detected in skill tree")
        list.append(s.pk)
        s = s.parent

@receiver(post_save, sender=Skill)
def add_child_to_lists(sender, instance, skill_pk=None, **kwargs):
    if skill_pk is None:
        skill_pk = instance.pk
        remove_child_from_lists(sender=None, instance=None, skill_pk=skill_pk)

    l = [] if instance.children_list == "" else instance.children_list.split(',')
    if str(skill_pk) not in l:
        l.append(str(skill_pk))
    Skill.objects.filter(pk=instance.pk).update(children_list=",".join(l))

    if instance.parent is not None:
        add_child_to_lists(sender=None, instance=instance.parent, skill_pk=skill_pk)

@receiver(pre_delete, sender=Skill)
def remove_child_from_lists(sender, instance, skill_pk=None, **kwargs):
    if skill_pk is None:
        skill_pk = instance.pk
    for s in Skill.objects.filter(children_list__contains=str(skill_pk)):
        l = s.children_list.split(',')
        if str(skill_pk) in l:
            l.remove(str(skill_pk))
        Skill.objects.filter(pk=s.pk).update(children_list=",".join(l))


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
