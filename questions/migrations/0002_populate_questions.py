# -*- coding: utf-8 -*-
from south.v2 import DataMigration


class Migration(DataMigration):

    def forwards(self, orm):
        # Simulators:
        # -----------
        free_answer = orm.Simulator(name='free_answer', note='Written answer')
        free_answer.save()
        counting = orm.Simulator(name='counting', note='Counting objects')
        counting.save()
        selecting = orm.Simulator(name='selecting',
                                  note='Selecting specified number of objects')
        selecting.save()
        example_sim = orm.Simulator(name='example', note='Just an example')
        example_sim.save()
        # Numbers:
        # --------
        for n in range(1, 101):
            skill = orm['model.Skill'].objects.get(name=str(n))
            # for numbers up to 7 ... choice up to 10
            # for numbers up to 17 ... choice up to 20
            # for numbers above .... choice up to a 100
            nr = 1 if n <= 7 else 2 if n <= 17 else 10
            # number -> select objects
            orm.Question(type='c', skill=skill, player=selecting,
                         data='{"question": %s, "answer": %s, "nrows": %s, '
                         '"ncols": 10}' % (n, n, nr)).save()
            # objects -> number
            orm.Question(type='c', skill=skill, player=counting,
                         data='{"question": [%s], "answer": "%s", '
                         '"width": 10}' % (n, n)).save()
        # Addition:
        # ---------
        for a in range(1, 21):
            for b in range(1, 21):
                total = a + b
                if total <= 20:
                    x, y = (a, b) if a <= b else (b, a)
                    skill = orm['model.Skill'].objects.get(name='%s+%s' % (x, y))
                    orm.Question(type='c', skill=skill, player=free_answer,
                                 data='{"question": "%s+%s", "answer": "%s"}' % (a, b, total)).save()
                    orm.Question(type='c', skill=skill, player=counting,
                                 data='{"question": [%s, "+", %s], "answer": "%s", "width": 10}' % (a, b, total)).save()
        skill = orm['model.Skill'].objects.get(name='addition <= 100')
        for a in range(1, 100):
            for b in range(1, 100):
                total = a + b
                if total > 20 and total <= 100:
                    orm.Question(type='c', skill=skill, player=free_answer,
                                 data='{"question": "%s+%s", "answer": "%s"}' % (a, b, total)).save()
        # Multiplication:
        # ---------------
        for a in range(11):
            for b in range(11):
                total = a * b
                x, y = (a, b) if a <= b else (b, a)
                skill = orm['model.Skill'].objects.get(name='%sx%s' % (x, y))
                orm.Question(type='c', skill=skill, player=free_answer,
                             data='{"question": "%sx%s", "answer": "%s"}' % (a, b, total)).save()
        for a in range(11):
            for b in range(11, 21):
                total = a * b
                skill = orm['model.Skill'].objects.get(name='%sx%s' % (x, y))
                orm.Question(type='c', skill=skill, player=free_answer,
                             data='{"question": "%sx%s", "answer": "%s"}' % (a, b, total)).save()
                orm.Question(type='c', skill=skill, player=free_answer,
                             data='{"question": "%sx%s", "answer": "%s"}' % (b, a, total)).save()




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
            'children_list': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['model.Skill']"})
        },
        u'questions.answer': {
            'Meta': {'object_name': 'Answer'},
            'correctly_solved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['questions.Question']"}),
            'solving_time': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'questions.question': {
            'Meta': {'object_name': 'Question'},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questions.Simulator']"}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['model.Skill']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'c'", 'max_length': '1'})
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
