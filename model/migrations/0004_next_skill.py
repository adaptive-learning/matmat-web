# -*- coding: utf-8 -*-
from django.core.management import call_command
from south.v2 import DataMigration
from questions.migrations import load_data


class Migration(DataMigration):

    def forwards(self, orm):
        load_data('model/migrations/next_skill.json', orm)

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        u'model.skill': {
            'Meta': {'object_name': 'Skill'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['model.Skill']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['model']
    symmetrical = True
