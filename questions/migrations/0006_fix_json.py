# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import models, migrations


def fix_log_json(apps, schema_editor):
    Answer = apps.get_model("questions", "Answer")
    for answer in Answer.objects.all():
        answer.log = answer.log\
            .replace("u'", '"')\
            .replace("']", '"]')\
            .replace('u"', '"')\
            .decode('unicode-escape')\
            .replace('\\"', '\\\\"')\
            .replace('\\', '\\\\')\
            .replace('None', 'null')
        json.loads(answer.log)
        answer.save()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_fill_missing_answers'),
    ]

    operations = [
        migrations.RunPython(fix_log_json),
    ]
