# -*- coding: utf-8 -*-
from south.v2 import DataMigration
from model.migrations import get_children


class Migration(DataMigration):

    def forwards(self, orm):
        # Adam and Eve of all skills:
        math = orm.Skill(name='math', parent=None, level=1, note='Superskill')
        math.save()
        # addition:
        addition = orm.Skill(name='addition', parent=math, level=2,
                             note='Addition')
        addition.save()
        # addition up to 10
        a1 = orm.Skill(name='addition <= 10', parent=addition, level=3,
                       note='Addition with total up to 10')
        a1.save()
        for total in range(1, 11):
            for a in range(total / 2 + 1):
                b = total - a
                orm.Skill(name='%s+%s' % (a, b), parent=a1, level=4,
                          note='%s+%s' % (a, b)).save()
        # addition up to 20
        a2 = orm.Skill(name='addition <= 20', parent=addition, level=3,
                       note='Addition with total up to 20')
        a2.save()
        for total in range(11, 21):
            for a in range(total / 2 + 1):
                b = total - a
                orm.Skill(name='%s+%s' % (a, b), parent=a2, level=4,
                          note='%s+%s' % (a, b)).save()
        # addition up to 100
        a3 = orm.Skill(name='addition <= 100', parent=addition, level=3,
                       note='Addition with total up to 100')
        a3.save()
        # addition up to 1000
        a4 = orm.Skill(name='addition <= 1000', parent=addition, level=3,
                       note='Addition with total up to 1000')
        a4.save()
        # numbers:
        numbers = orm.Skill(name='numbers', parent=math, level=2,
                            note='Numbers')
        numbers.save()
        num10 = orm.Skill(name='numbers <= 10', parent=numbers, level=3,
                          note='Numbers up to 10')
        num10.save()
        num20 = orm.Skill(name='numbers <= 20', parent=numbers, level=3,
                          note='Numbers up to 20')
        num20.save()
        num100 = orm.Skill(name='numbers <= 100', parent=numbers, level=3,
                           note='Numbers up to 100')
        num100.save()
        for n in range(1, 101):
            if n <= 10:
                p = num10
            elif n <= 20:
                p = num20
            else:
                p = num100
            orm.Skill(name=str(n), parent=p, level=4, note=str(n)).save()
        #  update children
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
