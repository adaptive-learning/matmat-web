# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fix_log_typo(apps, schema_editor):
    Answer = apps.get_model("questions", "Answer")
    for answer in Answer.objects.filter(log__contains='kyeborad'):
        answer.log = answer.log.replace("kyeborad", "keyboard")
        answer.save()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_delete_duplicit_answers'),
    ]

    operations = [
        migrations.RunPython(fix_log_typo),
    ]
