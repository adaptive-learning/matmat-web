# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from model.utils import recalculate_model


def delete_duplicit_answers(apps, schema_editor):
    Answer = apps.get_model("questions", "Answer")
    for answer in Answer.objects.filter(log__regex='finished.*finished'):
        original_answer_count = Answer.objects.filter(
            user=answer.user, question=answer.question,
            pk__gt=answer.pk-100, pk__lt=answer.pk+100).exclude(pk=answer.pk).count()
        if original_answer_count != 0:
            answer.delete()
        else:
            print "keeping answer", answer.pk

    recalculate_model()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_question_identifier'),
    ]

    operations = [
        migrations.RunPython(delete_duplicit_answers),
    ]
