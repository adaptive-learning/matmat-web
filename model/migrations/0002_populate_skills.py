# -*- coding: utf-8 -*-
from south.v2 import DataMigration
from model.migrations import get_children


class Migration(DataMigration):

    def forwards(self, orm):
        # abbreviations
        skill_level = {}

        def S(name, parent, note=None):
            level = 1 if parent is None else skill_level[parent.name] + 1
            skill_level[name] = level
            note = name if note is None else note
            s = orm.Skill(name=name, parent=parent, level=level, note=note)
            s.save()
            return s

        # Main math skill:
        # ----------------
        math = S(name='math', parent=None, note='Všechno')

        # Numbers:
        # --------
        numbers = S(name='numbers', parent=math, note='Počítání')
        num10 = S(name='numbers <= 10', parent=numbers, note='Počítání do 10')
        num20 = S(name='numbers <= 20', parent=numbers, note='Počítání do 20')
        num100 = S(name='numbers <= 100', parent=numbers,
                   note='Počítání do 100')
        for n in range(1, 101):
            S(name=str(n),
              parent=num10 if n <= 10 else (num20 if n <= 20 else num100),
              note=str(n))

        # Addition:
        # ---------
        addition = S(name='addition', parent=math, note=u'Sčítání')
        a1 = S(name='addition <= 10', parent=addition, note=u'Sčítání do 10')
        a2 = S(name='addition <= 20', parent=addition, note=u'Sčítání do 20')
        S(name='addition <= 100', parent=addition, note=u'Sčítání do 100')
        for a in range(20):
            for b in range(a, 21):
                if a + b <= 20:
                    S(name='%s+%s' % (a, b), parent=a1 if a + b <= 10 else a2)

        # Subtraction:
        # ------------
        subtr = S(name='subtraction', parent=math, note=u'Odčítání')
        s1 = S(name='subtraction <= 10', parent=subtr, note=u'Odčítání do 10')
        s2 = S(name='subtraction <= 20', parent=subtr, note=u'Odčítání do 20')
        for a in range(1, 21):
            for b in range(1, a + 1):
                S(name='%s-%s' % (a, b), parent=s1 if a <= 10 else s2)

        # Multiplication:
        # ---------------
        m0 = S(name='multiplication', parent=math, note=u'Násobení')
        m1 = S(name='multiplication1', parent=m0, note=u'Malá násobilka')
        for b in range(11):
            for a in range(b + 1):
                S(name='%sx%s' % (a, b), parent=m1)
        m2 = S(name='multiplication2', parent=m0, note=u'Velká násobilka')
        for a in range(11):
            for b in range(11, 21):
                S(name='%sx%s' % (a, b), parent=m2)

        # Division:
        # ---------
        d0 = S(name='division', parent=math, note=u'Dělení')
        d1 = S(name='division1', parent=d0, note=u'Dělení malých čísel')
        for a in range(11):
            for b in range(1, 11):
                total = a * b
                S(name='%s/%s' % (total, b), parent=d1)

        #  update children
        #-----------------
        for s in orm.Skill.objects.all():
            pk = s.pk
            list = ",".join([str(s.pk) for s in get_children(s)])
            orm.Skill.objects.filter(pk=pk).update(children_list=list)

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
        u'model.questiondifficulty': {
            'Meta': {'object_name': 'QuestionDifficulty'},
            'question': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'difficulty'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['questions.Question']"}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0'})
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
        u'model.userskill': {
            'Meta': {'unique_together': "(('user', 'skill'),)", 'object_name': 'UserSkill'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['model.Skill']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0'})
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

    complete_apps = ['model']
    symmetrical = True
