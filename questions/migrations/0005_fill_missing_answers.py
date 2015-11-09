# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from django.db import models, migrations


def fill_missing_answers(apps, schema_editor):
    Answer = apps.get_model("questions", "Answer")
    print
    for answer in Answer.objects.filter(pk__lt=429, answer__isnull=True):
        answer_value = re.findall(r'u\'(\d+)\'\], \[\d+, u\'finished', answer.log)
        if len(answer_value) == 1:
            answer.answer = answer_value[0]
            answer.save()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_fix_typo'),
    ]

    operations = [
        migrations.RunPython(fill_missing_answers),
    ]
