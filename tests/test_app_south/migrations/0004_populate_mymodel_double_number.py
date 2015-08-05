# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.db.models import F

class Migration(DataMigration):

    def forwards(self, orm):
        MyModel = orm.MyModel
        MyModel.objects.update(double_number=models.F('number')*2)

    def backwards(self, orm):
        "Write your backwards methods here."

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
    symmetrical = True
