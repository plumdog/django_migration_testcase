# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MyModel.double_number'
        db.add_column(u'test_app_south_mymodel', 'double_number',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MyModel.double_number'
        db.delete_column(u'test_app_south_mymodel', 'double_number')


    models = {
        u'test_app_south.mymodel': {
            'Meta': {'object_name': 'MyModel'},
            'double_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['test_app_south']