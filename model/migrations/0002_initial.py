# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '__first__'),
        ('model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionDifficulty',
            fields=[
                ('question', models.OneToOneField(related_name='difficulty', primary_key=True, serialize=False, to='questions.Question')),
                ('value', models.FloatField(default=0)),
                ('time_intensity', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField(default=0)),
                ('skill', models.ForeignKey(related_name='user_skills', to='model.Skill')),
                ('user', models.ForeignKey(related_name='user_skills', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userskill',
            unique_together=set([('user', 'skill')]),
        ),
    ]
