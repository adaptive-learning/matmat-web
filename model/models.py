from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from core.models import UserProfile, is_user_registred
from elo.DataProviderInterface import DataProviderInterface
from matmat import settings
from questions.models import Answer


class Skill(models.Model):
    name = models.CharField(max_length=30, unique=True)
    note = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="children")
    level = models.IntegerField()
    children_list = models.TextField(default="")
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def get_image_name(self, user):
        graphics = user.profile.graphics if is_user_registred(user) else settings.DEFAULT_GRAPHICS
        if graphics == UserProfile.PLAIN:
            return "graphics/plain/skill_{}.png".format(self.name)
        if graphics == UserProfile.WIZARD:
            return "graphics/wizard/skill_{}.png".format(self.name)

    def get_answers_count(self, user, correctly_solved=None):
        answers = Answer.objects.filter(question__skill__in=self.children_list.split(","), user=user)
        if correctly_solved is not None:
            answers = answers.filter(correctly_solved=correctly_solved)
        return answers.count()

    def active_children(self):
        return self.children.filter(active=True)

    def active_children_list(self):
        # TODO - caching
        deactivated_skills = set([pk for skill in Skill.objects.filter(active=False) for pk in skill.children_list.split(",")])
        return set(self.children_list.split(",")) - deactivated_skills


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
    time_intensity = models.FloatField(default=0.)

    def __unicode__(self):
        return self.value

    def get_first_attempts_count(self):
        return self.question.answers.values('user').distinct().count()

    def get_attempts_count(self):
        return self.question.answers.count()

    def get_average_answer_time(self):
        if self.question.answers.count() == 0:
            return None
        return self.question.answers.aggregate(Avg('solving_time'))

class UserSkill(models.Model):
    user = models.ForeignKey(User, related_name="user_skills")
    skill = models.ForeignKey(Skill, related_name="user_skills")
    value = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'skill')


class DatabaseDataProvider(DataProviderInterface):
    def get_question(self, answer):
        return answer.question

    def get_user(self, answer):
        return answer.user

    def get_skill(self, question):
        return question.skill

    def get_question_type(self, question):
        return question.type

    def get_user_skill(self, user, skill):
        try:
            return UserSkill.objects.get(user=user, skill=skill).value
        except UserSkill.DoesNotExist:
            return None

    def set_user_skill(self, user, skill, value):
        user_skill, _ = UserSkill.objects.get_or_create(user=user, skill=skill)
        user_skill.value = value
        user_skill.save()

    def get_parent_skill(self, skill):
        return skill.parent

    def get_difficulty(self, question):
        try:
            difficulty = question.difficulty.value
        except QuestionDifficulty.DoesNotExist:
            difficulty = None
        return difficulty

    def set_difficulty(self, question, value):
        difficulty, _ = QuestionDifficulty.objects.get_or_create(question=question)
        difficulty.value = value
        difficulty.save()

    def get_solving_time(self, answer):
        return answer.solving_time

    def get_correctness(self, answer):
        return answer.correctly_solved

    def is_first_attempt(self, answer):
        return answer.is_first_attempt()

    def get_first_attempts_count(self, question):
        return question.difficulty.get_first_attempts_count()

    def get_attempts_count(self, question):
        return question.difficulty.get_attempts_count()

    def get_time_intensity(self, question):
        try:
            difficulty = question.difficulty.time_intensity
        except QuestionDifficulty.DoesNotExist:
            difficulty = None
        return difficulty

    def set_time_intensity(self, question, value):
        difficulty, _ = QuestionDifficulty.objects.get_or_create(question=question)
        difficulty.time_intensity = value
        difficulty.save()