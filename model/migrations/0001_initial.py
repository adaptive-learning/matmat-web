# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('note', models.TextField(null=True, blank=True)),
                ('level', models.IntegerField()),
                ('children_list', models.TextField(default=b'')),
                ('active', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='model.Skill', null=True)),
            ],
        ),
    ]
