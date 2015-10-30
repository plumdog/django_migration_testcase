# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NonNullableForeignModel'
        db.create_table(u'test_app_nonnullableforeignmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('my', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['test_app.MyModel'], null=True, blank=True)),
        ))
        db.send_create_signal(u'test_app', ['NonNullableForeignModel'])

    def backwards(self, orm):
        # Deleting model 'NonNullableForeignModel'
        db.delete_table(u'test_app_nonnullableforeignmodel')

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
        u'test_app.nonnullableforeignmodel': {
            'Meta': {'object_name': 'NonNullableForeignModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'my': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['test_app.MyModel']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'test_app.nullableforeignmodel': {
            'Meta': {'object_name': 'NullableForeignModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'my': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['test_app.MyModel']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['test_app']
