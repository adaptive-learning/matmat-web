# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table(u'questions_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Simulator'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['model.Skill'])),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'questions', ['Question'])

        # Adding model 'Simulator'
        db.create_table(u'questions_simulator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'questions', ['Simulator'])


    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table(u'questions_question')

        # Deleting model 'Simulator'
        db.delete_table(u'questions_simulator')


    models = {
        u'model.skill': {
            'Meta': {'object_name': 'Skill'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['model.Skill']", 'null': 'True'})
        },
        u'questions.simulator': {
            'Meta': {'object_name': 'Simulator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'questions.question': {
            'Meta': {'object_name': 'Question'},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questions.Simulator']"}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['model.Skill']"})
        }
    }

    complete_apps = ['questions']
