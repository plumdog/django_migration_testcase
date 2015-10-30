# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'NullableForeignModel.my'
        db.alter_column(u'test_app_nullableforeignmodel', 'my_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['test_app.MyModel'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'NullableForeignModel.my'
        # raise RuntimeError("Cannot reverse this migration. 'NullableForeignModel.my' and its values cannot be restored.")

        # The following code is provided here to aid in writing a correct migration
        # Changing field 'NullableForeignModel.my'
        db.alter_column(u'test_app_nullableforeignmodel', 'my_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['test_app.MyModel']))

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
        u'test_app.nullableforeignmodel': {
            'Meta': {'object_name': 'NullableForeignModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'my': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['test_app.MyModel']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['test_app']
