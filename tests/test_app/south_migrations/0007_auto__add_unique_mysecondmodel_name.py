# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'MySecondModel', fields ['name']
        db.create_unique('test_app_mysecondmodel', ['name'])

    def backwards(self, orm):
        # Removing unique constraint on 'MySecondModel', fields ['name']
        db.delete_unique('test_app_mysecondmodel', ['name'])

    models = {
        'test_app.foreignmodel': {
            'Meta': {'object_name': 'ForeignModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'my': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_app.MyModel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'test_app.mymodel': {
            'Meta': {'object_name': 'MyModel'},
            'double_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'test_app.mysecondmodel': {
            'Meta': {'object_name': 'MySecondModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['test_app']
