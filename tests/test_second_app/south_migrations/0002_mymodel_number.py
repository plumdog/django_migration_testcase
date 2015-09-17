# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MyModel.number'
        db.add_column(u'test_second_app_mymodel', 'number',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'MyModel.number'
        db.delete_column(u'test_second_app_mymodel', 'number')

    models = {
        u'test_second_app.mymodel': {
            'Meta': {'object_name': 'MyModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['test_second_app']
