from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=30)
    note = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("model.Skill", null=True)
