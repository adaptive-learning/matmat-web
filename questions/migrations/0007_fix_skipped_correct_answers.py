# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import  migrations

from model.utils import recalculate_model


def fix_skipped_correct_answers(apps, schema_editor):
    Question = apps.get_model("questions", "Question")
    expected_answers = {q.pk: unicode(json.loads(q.data)["answer"]) for q in Question.objects.all()}

    Answer = apps.get_model("questions", "Answer")
    for answer in Answer.objects.all():
        log = json.loads(answer.log)
        if len(log) > 2 and log[-2][1] == 'skipped' and unicode(log[-3][1]) == expected_answers[answer.question_id]:
            answer.correctly_solved = True
            answer.answer = expected_answers[answer.question_id]
            answer.save()

    print "recalculating model..."
    recalculate_model()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_fix_json'),
    ]

    operations = [
        migrations.RunPython(fix_skipped_correct_answers),
    ]
