# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
import json
import random

class Migration(DataMigration):

    def forwards(self, orm):
        sim = orm.Simulator(name='moving', note='Přesunování')
        sim.save()

        SKILLS = {}

        def get_skill(name):
            if name not in SKILLS:
                SKILLS[name] = orm['model.Skill'].objects.get(name=name)
            return SKILLS[name]

        def Q(skill, data, value=4):
            data = json.dumps(data) if isinstance(data, dict) else data
            skill = get_skill(skill) if isinstance(skill, str) else skill
            q = orm.Question(type='c', skill=skill, player=sim, data=data, value=value)
            q.save()
            return q

        random.seed(12345)
        skill = 'numbers <= 10'
        token_list = [range(1, 4), range(1, 6), range(1, 10, 2), range(2, 10, 2),
                      [2, 3, 5, 7], range(2, 11, 2), range(6, 10), [1, 5, 6, 9, 10],
                      range(3, 8), [2, 3, 7, 9, 10]]
        for tokens in token_list:
            val = max(tokens)
            tokens = map(str, tokens)
            ans = [t for t in tokens]
            random.shuffle(tokens)
            Q(skill, {'tokens': tokens, 'answer': [ans], 'nboxes': 1, 'free_answer': False}, val)

        sim = orm.Simulator(name='choice', note='Výběr z možností')
        sim.save()

        l = range(1, 11)
        tokens = set()
        while len(tokens) < 10:
            x = tuple(sorted(random.sample(l, 2)))
            tokens.add(x)
        for tok in tokens:
            val = max(tok)
            tok = map(str, tok)
            random.shuffle(tok)
            Q(skill, {'tokens': tok, 'answer': str(val), 'text': 'Vyber vetší číslo'}, val)

        tokens = set()
        while len(tokens) < 5:
            x = tuple(sorted(random.sample(l, 3)))
            tokens.add(x)
        while len(tokens) < 10:
            x = tuple(sorted(random.sample(l, 4)))
            tokens.add(x)
        for tok in tokens:
            val = max(tok)
            tok = map(str, tok)
            random.shuffle(tok)
            Q(skill, {'tokens': tok, 'answer': str(val), 'text': 'Vyber nejvetší číslo'}, val)


    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'model.skill': {
            'Meta': {'object_name': 'Skill'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'children_list': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['model.Skill']"})
        },
        u'questions.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'correctly_solved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'device': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['questions.Question']"}),
            'solving_time': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['auth.User']"})
        },
        u'questions.question': {
            'Meta': {'object_name': 'Question'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['questions.Simulator']"}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['model.Skill']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'c'", 'max_length': '1'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'questions.simulator': {
            'Meta': {'object_name': 'Simulator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['questions']
    symmetrical = True
