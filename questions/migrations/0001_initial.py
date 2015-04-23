# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log', models.TextField()),
                ('solving_time', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('correctly_solved', models.BooleanField(default=False)),
                ('answer', models.CharField(max_length=255, null=True)),
                ('device', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.TextField(verbose_name=b'Data as JSON')),
                ('type', models.CharField(default=b'c', max_length=1, choices=[(b't', b'time'), (b'c', b'correctness')])),
                ('value', models.CharField(max_length=255, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Simulator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('note', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='player',
            field=models.ForeignKey(related_name='questions', verbose_name=b'Simulator', to='questions.Simulator'),
        ),
        migrations.AddField(
            model_name='question',
            name='skill',
            field=models.ForeignKey(related_name='questions', to='model.Skill'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='questions.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(related_name='answers', to=settings.AUTH_USER_MODEL),
        ),
    ]
