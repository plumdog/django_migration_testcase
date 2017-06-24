# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MySecondModel'
        db.create_table('test_app_mysecondmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('test_app', ['MySecondModel'])

    def backwards(self, orm):
        # Deleting model 'MySecondModel'
        db.delete_table('test_app_mysecondmodel')

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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['test_app']
