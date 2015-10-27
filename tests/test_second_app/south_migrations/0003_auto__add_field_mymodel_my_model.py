# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MyModel.my_model'
        db.add_column(u'test_second_app_mymodel', 'my_model',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['test_app.MyModel'], null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'MyModel.foreign'
        db.delete_column(u'test_second_app_mymodel', 'my_model_id')

    models = {
        u'test_app.foreignmodel': {
            'Meta': {'object_name': 'ForeignModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'my': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['test_app.MyModel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'test_app.mymodel': {
            'Meta': {'object_name': 'MyModel'},
            'double_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'test_second_app.mymodel': {
            'Meta': {'object_name': 'MyModel'},
            'my_model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['test_app.MyModel']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['test_second_app']
